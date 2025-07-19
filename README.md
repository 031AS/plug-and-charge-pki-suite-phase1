# plug-and-charge-pki-suite-phase1
# 031AS Plug & Charge PKI Suite (Phase 1)

A local simulation toolkit for ISO 15118 Plug & Charge, built in Python. Includes full PKI trust chain, certificate management, revocation handling (CRL + OCSP), and TLS handshake simulation.

---

## 🚀 Features
- EVCC / SECC certificate generation
- Sub-CA and Root CA simulation
- Certificate revocation + OCSP responder
- TLS handshake with full trust chain
- GUI with visual trust graph and side panel
- CLI for revocation / unrevocation
- Contract validation for roaming support (EMAID)

---

## 🛠 Requirements
- Python 3.10+
- `pip install -r requirements.txt`

Recommended Python packages:
flask
cryptography
networkx
matplotlib
requests
tk


---

## 📁 Folder Structure
main.py
gui/ # Graphical trust chain + cert panel
cli/ # CLI revocation/unrevocation
pki/ # Cert generation utilities
ocsp/ # OCSP responder + JSON DB
tls/ # TLS handshake simulator
contracts/ # EMAID contract validator
utils/ # CRL + OCSP functions
certificates/ # Your generated certs


---

## ▶️ Running the App

### Start GUI:
```bash
$ python main.py


#### Start OCSP Responder:
$ python ocsp/ocsp_responder_real.py


### Use CLI for revocation:
$ MODE=cli python main.py
> revoke 6a94e7...      # Revoke a cert
> unrevoke 6a94e7...    # Restore it


### 📦 Certificate Handling
$ python pki/generate_certificates.py

Certificates will be stored in /certificates/ as:

root_ca.pem, root_ca.key
subca_ev.pem, subca_ev.key
evcc1.pem, secc1.pem, etc.

####  TLS Handshake Test
Open GUI and run TLS simulator
Or manually:

$ python tls/handshake_simulator.py

Listen on port 8443, wait for EV client to connect.
Use browser or custom EV TLS client.

📋 Notes
GUI includes branding "031AS" and trust chain visualization.

OCSP responder reloads cert_db.json live.

Supports multiple OEMs and CPOs.

🧪 Upcoming in Phase 2
REST APIs for certificate issuance

Google Cloud deployment

Full Hubject OPCP and ISO 15118-2 audit

OCPP integration (contract validation)


---













