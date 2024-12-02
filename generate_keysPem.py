from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64


private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()


# generating private pem
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# generating public pem
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# converting public pem to base64
public_pem_b64 = base64.urlsafe_b64encode(public_pem)

with open('private.pem', 'wb') as file:
    file.write(private_pem)
    
with open('public.pem', 'wb') as file:
    file.write(public_pem)
    file.write(f'\n\n\n\nBASE64 PUB KEY: {public_pem_b64}'.encode())
