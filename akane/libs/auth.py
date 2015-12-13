from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import cryptography.exceptions


def _get_privatekey():
    # TODO: 
    # read ssh key from user-defined file
    # handle encrypted keys
    with open('/home/mescam/.ssh/id_rsa', 'rb') as kfile:
        pk = serialization.load_pem_private_key(
                kfile.read(),
                password=None,
                backend=default_backend()
                )
        return pk

def _get_publickey():
    # TODO: 
    # read ssh key from user-defined file
    with open('/home/mescam/.ssh/id_rsa.pub', 'rb') as kfile:
        pk = serialization.load_ssh_public_key(
                kfile.read(),
                backend=default_backend()
                )
        return pk

def sign(message):
    pk = _get_privatekey()
    signer = pk.signer(
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
                ),
            hashes.SHA256()
            )
    signer.update(message)
    return signer.finalize()

def verify(signature, message):
    pk = _get_publickey()
    verifier = pk.verifier(
            signature,
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
