# pki/generate_certificates.py
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import os

def generate_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)

def create_self_signed_cert(subject_name, key, days=365):
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject_name)])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=days))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )
    return cert

def save_cert_and_key(cert, key, cert_path, key_path):
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def generate_root_ca(output_dir):
    key = generate_key()
    cert = create_self_signed_cert("031AS Root CA", key)
    os.makedirs(output_dir, exist_ok=True)
    save_cert_and_key(cert, key, os.path.join(output_dir, "root_ca.pem"), os.path.join(output_dir, "root_ca.key"))

