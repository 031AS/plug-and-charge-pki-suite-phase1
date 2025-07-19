# ocsp/ocsp_responder_real.py
import json
from flask import Flask, request, Response
from cryptography.x509.ocsp import load_der_ocsp_request, OCSPResponseBuilder, OCSPResponseStatus
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import AuthorityInformationAccessOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

app = Flask(__name__)
OCSP_PORT = 8888
CERT_DB_PATH = "ocsp/cert_db.json"

def load_cert_db():
    with open(CERT_DB_PATH, "r") as f:
        return json.load(f)

def get_cert_status(serial_hex, db):
    return db.get(serial_hex.lower(), "unknown")

@app.route("/", methods=["POST"])
def handle_ocsp():
    try:
        req_data = request.data
        ocsp_req = load_der_ocsp_request(req_data)
        serial = format(ocsp_req.serial_number, 'x')
        cert_db = load_cert_db()
        status = get_cert_status(serial, cert_db)

        if status == "revoked":
            builder = OCSPResponseBuilder().add_response(
                cert=ocsp_req.cert,
                issuer=ocsp_req.issuer,
                algorithm=hashes.SHA256(),
                cert_status='revoked',
                this_update=datetime.datetime.utcnow(),
                next_update=datetime.datetime.utcnow() + datetime.timedelta(days=1),
                revocation_time=datetime.datetime.utcnow()
            )
        elif status == "good":
            builder = OCSPResponseBuilder().add_response(
                cert=ocsp_req.cert,
                issuer=ocsp_req.issuer,
                algorithm=hashes.SHA256(),
                cert_status='good',
                this_update=datetime.datetime.utcnow(),
                next_update=datetime.datetime.utcnow() + datetime.timedelta(days=1)
            )
        else:
            builder = OCSPResponseBuilder().response_status(OCSPResponseStatus.UNAUTHORIZED)

        ocsp_resp = builder.sign(responder_cert=None, responder_key=None, algorithm=hashes.SHA256(), backend=default_backend())
        return Response(ocsp_resp.public_bytes(), mimetype="application/ocsp-response")

    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    print(f"🟢 OCSP Responder ready at http://localhost:{OCSP_PORT}")
    app.run(port=OCSP_PORT)

