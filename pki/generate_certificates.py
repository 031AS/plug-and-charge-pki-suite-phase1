# pki/generate_certificates.py

import os
from datetime import datetime, timedelta, timezone
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)

def write_cert(cert, path):
    with open(path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

def write_key(key, path):
    with open(path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def build_cert(subject, issuer, pub_key, issuer_key, is_ca=False):
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(subject)
    builder = builder.issuer_name(issuer)
    builder = builder.public_key(pub_key)
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.not_valid_before(datetime.now(timezone.utc))
    builder = builder.not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
    builder = builder.add_extension(
        x509.BasicConstraints(ca=is_ca, path_length=None),
        critical=True
    )
    return builder.sign(private_key=issuer_key, algorithm=hashes.SHA256())

def name(cn):
    return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn)])

# Ensure output folder
os.makedirs("certificates", exist_ok=True)

# Root CA
root_key = generate_key()
root_subject = name("Root CA")
root_cert = build_cert(root_subject, root_subject, root_key.public_key(), root_key, is_ca=True)
write_key(root_key, "certificates/root_ca.key")
write_cert(root_cert, "certificates/root_ca.pem")

# Sub-CA for EVCC
subca_ev_key = generate_key()
subca_ev_subject = name("Sub-CA EV")
subca_ev_cert = build_cert(subca_ev_subject, root_subject, subca_ev_key.public_key(), root_key, is_ca=True)
write_key(subca_ev_key, "certificates/subca_ev.key")
write_cert(subca_ev_cert, "certificates/subca_ev.pem")

# Sub-CA for SECC
subca_secc_key = generate_key()
subca_secc_subject = name("Sub-CA SECC")
subca_secc_cert = build_cert(subca_secc_subject, root_subject, subca_secc_key.public_key(), root_key, is_ca=True)
write_key(subca_secc_key, "certificates/subca_secc.key")
write_cert(subca_secc_cert, "certificates/subca_secc.pem")

# EVCC certificate signed by Sub-CA EV
evcc_key = generate_key()
evcc_subject = name("EVCC Cert")
evcc_cert = build_cert(evcc_subject, subca_ev_subject, evcc_key.public_key(), subca_ev_key)
write_key(evcc_key, "certificates/evcc1.key")
write_cert(evcc_cert, "certificates/evcc1.pem")

# SECC certificate signed by Sub-CA SECC
secc_key = generate_key()
secc_subject = name("SECC Cert")
secc_cert = build_cert(secc_subject, subca_secc_subject, secc_key.public_key(), subca_secc_key)
write_key(secc_key, "certificates/secc1.key")
write_cert(secc_cert, "certificates/secc1.pem")

# Chain files
with open("certificates/chain_evcc.pem", "wb") as f:
    f.write(subca_ev_cert.public_bytes(serialization.Encoding.PEM))
    f.write(root_cert.public_bytes(serialization.Encoding.PEM))

with open("certificates/chain_secc.pem", "wb") as f:
    f.write(subca_secc_cert.public_bytes(serialization.Encoding.PEM))
    f.write(root_cert.public_bytes(serialization.Encoding.PEM))

print("✅ All certificates and chains generated in /certificates")
