import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import cryptography.exceptions
from getpass import getpass

__pk_passwd = None

def _get_privatekey(path):
    global __pk_passwd

    with open(path, 'rb') as kfile:
        pk_data = kfile.read()
        __pk_passwd = getpass(prompt="Enter passphrase for private key: ") \
                if __pk_passwd is None and "ENCRYPTED" in pk_data else None
        pk = serialization.load_pem_private_key(
                data=pk_data,
                password=__pk_passwd,
                backend=default_backend()
                )
        return pk

def _get_publickey(path):
    with open(path, 'rb') as kfile:
        pk = serialization.load_ssh_public_key(
                kfile.read(),
                backend=default_backend()
                )
        return pk

def sign(message, kpath):
    pk = _get_privatekey(kpath)
    signer = pk.signer(
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
                ),
            hashes.SHA256()
            )
    signer.update(message)
    return base64.b64encode(signer.finalize())

def verify(signature, message, kpath):
    pk = _get_publickey(kpath)
    verifier = pk.verifier(
            base64.b64decode(signature),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
                ),
            hashes.SHA256()
            )
    verifier.update(message)
    try:
        verifier.verify()
        return True
    except cryptography.exceptions.InvalidSignature:
        return False
