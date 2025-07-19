# tls/secc_server.py
import ssl
import socket

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="certificates/secc1.pem", keyfile="certificates/secc1.key")
context.load_verify_locations(cafile="certificates/root_ca.pem")
context.verify_mode = ssl.CERT_NONE  # In production: CERT_REQUIRED

bind_addr = ("localhost", 8443)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(bind_addr)
    sock.listen(5)
    print("🔌 SECC waiting for EV handshake on port 8443...")
    conn, addr = sock.accept()

    with context.wrap_socket(conn, server_side=True) as tls:
        print(f"✅ TLS Handshake with {addr}")
        print("🔐 Cipher:", tls.cipher())
        print("📜 Peer Cert:", tls.getpeercert())
