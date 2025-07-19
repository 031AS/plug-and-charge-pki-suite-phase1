# pki/reissue_secc_cert.py
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import os

# Paths
key_path = "certificates/secc1.key"
cert_path = "certificates/secc1.pem"

# ✅ Check key exists
if not os.path.exists(key_path):
    raise FileNotFoundError(f"Private key not found at: {key_path}")

# 🔐 Load existing SECC key
with open(key_path, "rb") as f:
    key = serialization.load_pem_private_key(f.read(), password=None)

# 🛡️ Create cert with CN = SECC
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"SECC"),
])
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    .sign(key, hashes.SHA256())
)

# 💾 Save cert
with open(cert_path, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print(f"✅ New SECC certificate written to {cert_path}")
