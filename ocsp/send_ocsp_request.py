# ocsp/send_ocsp_request.py
import requests
from cryptography import x509
from cryptography.x509.ocsp import OCSPRequestBuilder
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Load certificate and issuer (for OCSP request)
def load_cert(path):
    with open(path, 'rb') as f:
        return x509.load_pem_x509_certificate(f.read(), default_backend())

cert = load_cert("certificates/evcc1.pem")
issuer = load_cert("certificates/subca_ev.pem")

# Build OCSP request
builder = OCSPRequestBuilder()
builder = builder.add_certificate(cert, issuer, hashes.SHA256())
req = builder.build()
req_data = req.public_bytes(encoding=x509.Encoding.DER)

# Send request to local OCSP responder
url = "http://localhost:8888"
headers = {"Content-Type": "application/ocsp-request"}
print("📤 Sending OCSP request...")
resp = requests.post(url, data=req_data, headers=headers)

# Output
if resp.status_code == 200:
    print("✅ Response received:", resp.content.hex()[:60], "...")
else:
    print("❌ Failed:", resp.status_code, resp.text)
# ocsp/send_ocsp_request.py
import requests
from cryptography import x509
from cryptography.x509.ocsp import OCSPRequestBuilder
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def load_cert(path):
    with open(path, 'rb') as f:
        return x509.load_pem_x509_certificate(f.read(), default_backend())

cert = load_cert("certificates/evcc1.pem")
issuer = load_cert("certificates/subca_ev.pem")

builder = OCSPRequestBuilder()
builder = builder.add_certificate(cert, issuer, hashes.SHA256())
ocsp_req = builder.build()
req_data = ocsp_req.public_bytes(x509.Encoding.DER)

url = "http://localhost:8888"
headers = {"Content-Type": "application/ocsp-request"}
print("📤 Sending OCSP request...")

resp = requests.post(url, data=req_data, headers=headers)

if resp.status_code == 200:
    print(f"✅ Response received (hex): {resp.content.hex()[:60]}...")
else:
    print(f"❌ Failed: {resp.status_code}\n{resp.text}")
