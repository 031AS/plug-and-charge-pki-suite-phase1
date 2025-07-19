# pki/generate_certificates.py
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta, timezone
import os

CERT_DIR = "certificates"
os.makedirs(CERT_DIR, exist_ok=True)

def utc_now():
    return datetime.now(timezone.utc)

def generate_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)

def write_cert_and_key(cert, key, name):
    with open(f"{CERT_DIR}/{name}.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open(f"{CERT_DIR}/{name}.key", "wb") as f:
        f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        ))

def create_ca(name, issuer_key=None, issuer_name=None):
    key = generate_key()
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, name)])
    issuer = issuer_name if issuer_name else subject
    signer_key = issuer_key if issuer_key else key

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(utc_now())
        .not_valid_after(utc_now() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(signer_key, hashes.SHA256())
    )
    return cert, key, subject

def create_device_cert(name, issuer_cert, issuer_key):
    key = generate_key()
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, name)])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer_cert.subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(utc_now())
        .not_valid_after(utc_now() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(issuer_key, hashes.SHA256())
    )
    return cert, key

if __name__ == "__main__":
    # Root CA
    root_cert, root_key, root_subject = create_ca("031AS Root CA")
    write_cert_and_key(root_cert, root_key, "root_ca")

    # Sub-CAs
    sub_ev_cert, sub_ev_key, sub_ev_subject = create_ca("031AS Sub-CA EV", root_key, root_cert.subject)
    sub_evse_cert, sub_evse_key, sub_evse_subject = create_ca("031AS Sub-CA EVSE", root_key, root_cert.subject)
    write_cert_and_key(sub_ev_cert, sub_ev_key, "subca_ev")
    write_cert_and_key(sub_evse_cert, sub_evse_key, "subca_evse")

    # Device certs
    evcc_cert, evcc_key = create_device_cert("EVCC Cert 1", sub_ev_cert, sub_ev_key)
    secc_cert, secc_key = create_device_cert("SECC Cert 1", sub_evse_cert, sub_evse_key)
    write_cert_and_key(evcc_cert, evcc_key, "evcc1")
    write_cert_and_key(secc_cert, secc_key, "secc1")

    print("✅ All certificates generated with UTC timestamps.")
