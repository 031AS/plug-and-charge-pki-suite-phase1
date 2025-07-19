import ssl
import socket
import os

print("👀 SECC server script starting...")

def run_secc_server():
    host = "localhost"
    port = 8443

    # Path to server certificate and private key
    server_cert = "certificates/secc1.pem"
    server_key = "certificates/secc1.key"
    ca_chain = "certificates/chain_secc.pem"  # Contains Sub-CA + Root CA

    if not all(os.path.exists(p) for p in [server_cert, server_key, ca_chain]):
        print("❌ Missing one or more SECC certificate files.")
        return

    # Setup TLS context with mutual authentication disabled
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=server_cert, keyfile=server_key)
    context.load_verify_locations(cafile=ca_chain)

    bindsocket = socket.socket()
    bindsocket.bind((host, port))
    bindsocket.listen(5)

    print(f"🔌 SECC waiting for EV handshake on port {port}...")

    try:
        while True:
            conn, addr = bindsocket.accept()
            print(f"📥 Connection from {addr}")

            try:
                with context.wrap_socket(conn, server_side=True) as tls:
                    print(f"✅ TLS handshake successful.")
                    print(f"🔐 Cipher: {tls.cipher()}")
                    cert = tls.getpeercert()
                    print(f"📜 Client Cert: {cert}")
            except ssl.SSLError as e:
                print(f"❌ TLS handshake failed: {e}")
            finally:
                conn.close()

    except KeyboardInterrupt:
        print("🛑 SECC server stopped.")
