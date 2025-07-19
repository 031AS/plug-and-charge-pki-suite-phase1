# tls/handshake_simulator.py
import ssl
import socket
from datetime import datetime, timezone

def simulate_tls_handshake(certfile, keyfile, cafile):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    context.load_verify_locations(cafile=cafile)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('localhost', 8443))
        sock.listen(1)
        print("🚗 Waiting for EV to connect (TLS handshake on port 8443)...")
        conn, addr = sock.accept()
        with context.wrap_socket(conn, server_side=True) as ssock:
            print(f"✅ TLS Handshake Complete with {addr}")
            print(f"🔐 Cipher: {ssock.cipher()}")
            cert = ssock.getpeercert()

            # Print peer certificate time validation
            not_before = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
            not_after = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            now = datetime.now(timezone.utc)

            print(f"📄 Cert Validity: {not_before} → {not_after}")
            print(f"📅 Current UTC time: {now}")

            if now < not_before.replace(tzinfo=timezone.utc) or now > not_after.replace(tzinfo=timezone.utc):
                print("❌ Certificate is NOT currently valid.")
            else:
                print("✅ Certificate is currently valid.")
