# tls/handshake_simulator.py
import ssl
import socket

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
            print(f"📄 Peer cert subject: {ssock.getpeercert().get('subject')}")

