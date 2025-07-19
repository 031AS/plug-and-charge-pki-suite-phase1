# tls/secc_server.py

import ssl
import socket

def run_secc_server():
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        # 🔐 Load SECC server certificate and key
        context.load_cert_chain(
            certfile="certificates/secc1.pem",
            keyfile="certificates/secc1.key"
        )

        # ✅ Trust the full EVCC chain: subca_ev.pem + root_ca.pem
        context.load_verify_locations(cafile="certificates/chain_evcc.pem")

        # 🛡️ For testing: allow handshake even without client cert
        context.verify_mode = ssl.CERT_OPTIONAL

        bind_addr = ("localhost", 8443)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(bind_addr)
            sock.listen(1)
            print("🔌 SECC waiting for EV handshake on port 8443...")

            conn, addr = sock.accept()
            print(f"📥 Connection from {addr}")

            try:
                with context.wrap_socket(conn, server_side=True) as tls:
                    print(f"✅ TLS Handshake with {addr}")
                    print(f"🔐 Cipher: {tls.cipher()}")
                    print(f"📜 Peer Cert: {tls.getpeercert()}")
            except ssl.SSLError as ssl_error:
                print(f"❌ TLS error: {ssl_error}")

    except Exception as e:
        print(f"❌ SECC Server failed to start: {e}")

if __name__ == "__main__":
    run_secc_server()
