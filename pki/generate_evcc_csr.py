# pki/generate_evcc_csr.py

import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_evcc_csr(emaid: str, out_dir: str = "certificates"):
    os.makedirs(out_dir, exist_ok=True)

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    key_path = os.path.join(out_dir, "evcc.key")
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, emaid)
    ])
    csr = x509.CertificateSigningRequestBuilder().subject_name(subject).sign(key, hashes.SHA256())

    csr_path = os.path.join(out_dir, "evcc.csr")
    with open(csr_path, "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    return key_path, csr_path
