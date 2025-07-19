# tls/handshake_runner.py
import ssl
import socket

def run_tls_handshake_gui():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile="certificates/evcc1.pem", keyfile="certificates/evcc1.key")
    context.load_verify_locations(cafile="certificates/root_ca.pem")
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED

    try:
        with socket.create_connection(("localhost", 8443)) as sock:
            with context.wrap_socket(sock, server_hostname="SECC") as tls:
                print("✅ TLS handshake succeeded.")
                print("🔐 Cipher:", tls.cipher())
                print("📜 Server Cert:", tls.getpeercert())
    except Exception as e:
        print(f"❌ TLS handshake failed: {e}")
