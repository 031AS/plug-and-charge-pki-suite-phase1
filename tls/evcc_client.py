# tls/evcc_client.py
import ssl
import socket

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_cert_chain(certfile="certificates/evcc1.pem", keyfile="certificates/evcc1.key")
context.load_verify_locations(cafile="certificates/root_ca.pem")
context.check_hostname = False
context.verify_mode = ssl.CERT_REQUIRED

print("🚗 EV attempting to connect to SECC (localhost:8443)...")

with socket.create_connection(("localhost", 8443)) as sock:
    with context.wrap_socket(sock, server_hostname="SECC") as tls:
        print("✅ Handshake complete.")
        print("🔐 Cipher:", tls.cipher())
        print("📜 Peer Cert:", tls.getpeercert())
