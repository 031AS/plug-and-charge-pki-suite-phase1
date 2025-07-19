# tls/secc_server.py
import ssl
import socket

def run_secc_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="certificates/secc1.pem", keyfile="certificates/secc1.key")
    context.load_verify_locations(cafile="certificates/root_ca.pem")
    context.verify_mode = ssl.CERT_NONE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(("localhost", 8443))
        sock.listen(1)
        print("🔌 SECC waiting for EV handshake on port 8443...")
        conn, addr = sock.accept()
        with context.wrap_socket(conn, server_side=True) as tls:
            print(f"✅ TLS Handshake with {addr}")
            print(f"🔐 Cipher: {tls.cipher()}")
            print(f"📜 Peer Cert: {tls.getpeercert()}")

# 🟢 Add this block:
if __name__ == "__main__":
    run_secc_server()
