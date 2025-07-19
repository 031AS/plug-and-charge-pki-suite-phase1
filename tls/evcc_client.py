import ssl
import socket

def run_evcc_tls():
    print("🚗 EV attempting to connect to SECC (localhost:8443)...")

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    # Load EVCC client cert + key
    try:
        context.load_cert_chain(
            certfile="certificates/evcc1.pem",
            keyfile="certificates/evcc1.key"
        )
    except Exception as e:
        print(f"❌ Failed to load EVCC certificate/key: {e}")
        return

    # Load the CA chain that should validate SECC (Sub-CA + Root)
    try:
        context.load_verify_locations(cafile="certificates/chain_secc.pem")
    except Exception as e:
        print(f"❌ Failed to load SECC trust chain: {e}")
        return

    # Attempt TLS connection
    try:
        with socket.create_connection(("localhost", 8443)) as sock:
            with context.wrap_socket(sock, server_hostname="SECC") as tls:
                print("✅ TLS handshake succeeded.")
                print(f"🔐 Cipher: {tls.cipher()}")
                cert = tls.getpeercert()
                print(f"📜 Server Cert: {cert}")
    except ssl.SSLError as e:
        print(f"❌ TLS handshake failed: {e}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
