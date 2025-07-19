
# utils/crl_ocsp_utils.py
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import requests

def load_crl_from_file(path):
    with open(path, 'rb') as f:
        crl_data = f.read()
    return x509.load_pem_x509_crl(crl_data, default_backend())

def is_cert_revoked(cert, crl):
    for revoked in crl:
        if revoked.serial_number == cert.serial_number:
            return True
    return False

def ocsp_check(ocsp_url, ocsp_req_der):
    headers = {'Content-Type': 'application/ocsp-request'}
    resp = requests.post(ocsp_url, data=ocsp_req_der, headers=headers)
    if resp.status_code == 200:
        return resp.content
    return None
