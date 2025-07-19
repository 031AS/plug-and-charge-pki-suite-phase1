import ssl
import socket
import os

print("👀 SECC server script starting...")

def run_secc_server():
    host = "localhost"
    port = 8443

    # Certificate files
    server_cert = "certificates/secc1.pem"
    server_key = "certificates/secc1.key"
    ca_chain = "certificates/chain_secc.pem"

    print("📁 Checking certificate files...")
    print(f"🔍 secc1.pem exists: {os.path.exists(server_cert)}")
    print(f"🔍 secc1.key exists: {os.path.exists(server_key)}")
    print(f"🔍 chain_secc.pem exists: {os.path.exists(ca_chain)}")

    if not all(os.path.exists(p) for p in [server_cert, server_key, ca_chain]):
        print("❌ Missing one or more SECC certificate files.")
        return

    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=server_cert, keyfile=server_key)
        context.load_verify_locations(cafile=ca_chain)

        bindsocket = socket.socket()
        bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        bindsocket.bind((host, port))
        bindsocket.listen(5)

        print(f"🔌 SECC waiting for EV handshake on port {port}...")

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

    except Exception as e:
        print(f"❌ SECC Server failed to start: {e}")

if __name__ == "__main__":
    run_secc_server()

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
