import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID

def parse_cert(path):
    with open(path, "rb") as f:
        cert_data = f.read()
        return x509.load_pem_x509_certificate(cert_data, default_backend())

def update_trust_graph():
    print("🔍 Trust Chain Structure:\n")

    cert_paths = [
        "certificates/root_ca.pem",
        "certificates/subca_ev.pem",
        "certificates/evcc1.pem",
        "certificates/subca_secc.pem",
        "certificates/secc1.pem"
    ]

    for path in cert_paths:
        if os.path.exists(path):
            cert = parse_cert(path)
            subject = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            issuer = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            print(f"🔗 {subject}\n   ⬑ issued by: {issuer}\n")
        else:
            print(f"⚠️  Missing certificate file: {path}")

