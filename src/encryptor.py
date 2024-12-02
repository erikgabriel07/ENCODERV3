from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESSIV
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from hashlib import sha256
import os, io, struct, base64



class EncryptorManager:

    def encrypt_file(self, public_key, data, filename):
        
        # Gerando uma chave privada temporária
        ephemeral_private_key = ec.generate_private_key(ec.SECP256R1())
        ephemeral_public_key = ephemeral_private_key.public_key()
        
        # Calculado a chave compartilhada
        shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)
        
        # Gerando chave simétrica a partir da chave compartilhada
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'aes-siv-derived'
        ).derive(shared_key)

        # Gerando iv determinístico
        siv = AESSIV(derived_key)
        
        # Metadados opcionais
        file_hash = sha256(filename).hexdigest()
        file_hash = file_hash.encode()
        metadados = [file_hash]
        
        encrypted_data = siv.encrypt(data, associated_data=metadados)
        encrypted_filename = siv.encrypt(filename, associated_data=metadados)
        
        # Gerando pem da chave pública
        public_key_pem = ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        header = struct.pack('IIII', len(public_key_pem), len(encrypted_filename), len(encrypted_data), len(file_hash))
        
        result = header + public_key_pem + encrypted_filename + encrypted_data + file_hash
        
        return base64.urlsafe_b64encode(result), base64.urlsafe_b64encode(encrypted_filename)
        
        
    def decrypt_file(self, private_key, data):
        
        data = base64.urlsafe_b64decode(data)
        
        byte_stream = io.BytesIO(data)
        
        # Recuperando cabeçalho
        header = byte_stream.read(16); byte_stream.seek(16)
        data_pos = struct.unpack('IIII', header)
        
        # Recuperando chave pública e dados
        public_pem = byte_stream.read(data_pos[0])
        filename = byte_stream.read(data_pos[1])
        data = byte_stream.read(data_pos[2])
        file_hash = byte_stream.read(data_pos[3])
        
        # Carregando chave pública e chave compartilhada
        ephemeral_public_key = serialization.load_pem_public_key(public_pem)
        shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)
        
        # Gerando chave simétrica a partir da chave compartilhada
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'aes-siv-derived'
        ).derive(shared_key)
        
        # Gerando iv determinístico
        siv = AESSIV(derived_key)
        
        # Metadados opcionais
        metadados = [file_hash]
        
        decrypted_data = siv.decrypt(data, associated_data=metadados)
        decrypted_filename = siv.decrypt(filename, associated_data=metadados)
        
        return decrypted_data, decrypted_filename
        
    def encrypt_dir(self, dirname, key):
        """
        Método apenas para criptografia de arquivos.
        Esse método utiliza uma criptografia simples apenas
        para que todo o programa siga o contexto ao qual ele
        oferece. Esse método não garante que o nome dos diretórios
        não possam ser recuperados, uma vez que a chave simétrica
        está salva dentro da classe ProcessFiles e o resultado do nome
        do dirétorio encriptado não produz uma saída diferente para cada
        vez que o mesmo nome é encriptado.
        """
        
        key = base64.urlsafe_b64decode(key)
        
        padding_length = 16 - len(dirname) % 16
        padded_dirname = dirname + chr(padding_length) * padding_length
        
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        encryptor = cipher.encryptor()
        
        encrypted_dirname = encryptor.update(padded_dirname.encode()) + encryptor.finalize()
        
        return base64.urlsafe_b64encode(encrypted_dirname).decode()
        
    def decrypt_dir(self, encDirname, key):
        """Método para descriptografar o nome do diretório."""
        
        key = base64.urlsafe_b64decode(key)
        
        encDirname = base64.urlsafe_b64decode(encDirname)
        
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        decryptor = cipher.decryptor()
        
        decrypted_dirname = decryptor.update(encDirname) + decryptor.finalize()
        
        padding_length = decrypted_dirname[-1]
        original_name = decrypted_dirname[:-padding_length]
        
        return original_name