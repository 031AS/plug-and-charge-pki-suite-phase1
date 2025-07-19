import ssl
import socket

def run_evcc_tls():
    print("🚗 EV attempting to connect to SECC (localhost:8443)...")

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    try:
        context.load_cert_chain(
            certfile="certificates/evcc1.pem",
            keyfile="certificates/evcc1.key"
        )
    except Exception as e:
        print(f"❌ Failed to load EVCC cert/key: {e}")
        return

    try:
        context.load_verify_locations(cafile="certificates/chain_secc.pem")
    except Exception as e:
        print(f"❌ Failed to load SECC trust chain: {e}")
        return

    try:
        with socket.create_connection(("localhost", 8443)) as sock:
            with context.wrap_socket(sock, server_hostname="SECC") as tls:
                print("✅ Handshake complete.")
                print(f"🔐 Cipher: {tls.cipher()}")
                print(f"📜 Peer Cert: {tls.getpeercert()}")
    except ssl.SSLError as e:
        print(f"❌ TLS handshake failed: {e}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

__all__ = ['run_evcc_tls']
