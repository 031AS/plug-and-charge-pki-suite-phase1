import json
from flask import Flask, request, Response
from cryptography.x509.ocsp import load_der_ocsp_request, OCSPResponseBuilder, OCSPResponseStatus
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
OCSP_PORT = 8888
CERT_DB_PATH = "ocsp/cert_db.json"

def load_cert_db():
    with open(CERT_DB_PATH, "r") as f:
        return json.load(f)

@app.route("/", methods=["POST"])
def handle_ocsp():
    try:
        req_data = request.data
        ocsp_req = load_der_ocsp_request(req_data)
        serial = format(ocsp_req.serial_number, 'x').lower()

        cert_db = load_cert_db()
        status = cert_db.get(serial, "unknown")

        now = datetime.now(timezone.utc)
        builder = OCSPResponseBuilder()

        if status == "revoked":
            builder = builder.add_response(
                cert=ocsp_req.cert,
                issuer=ocsp_req.issuer,
                algorithm=hashes.SHA256(),
                cert_status='revoked',
                this_update=now,
                next_update=now + timedelta(days=1),
                revocation_time=now
            )
        elif status == "good":
            builder = builder.add_response(
                cert=ocsp_req.cert,
                issuer=ocsp_req.issuer,
                algorithm=hashes.SHA256(),
                cert_status='good',
                this_update=now,
                next_update=now + timedelta(days=1)
            )
        else:
            return Response("Unknown certificate", status=403)

        ocsp_resp = builder.sign(
            responder_cert=None,  # For real OCSP, include responder cert
            responder_key=None,
            algorithm=hashes.SHA256()
        )

        print(f"📥 Parsed OCSP request for serial: {serial}")
        print(f"✅ Responded with OCSP status: {status.upper()}")
        return Response(ocsp_resp.public_bytes(), mimetype="application/ocsp-response")

    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    print(f"🟢 OCSP Responder ready at http://localhost:{OCSP_PORT}")
    app.run(port=OCSP_PORT)
