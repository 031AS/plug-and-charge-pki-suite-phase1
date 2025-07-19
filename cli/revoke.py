# cli/revoke.py
import json
import os

CERT_DB_PATH = "ocsp/cert_db.json"

def load_db():
    if not os.path.exists(CERT_DB_PATH):
        return {}
    with open(CERT_DB_PATH, "r") as f:
        return json.load(f)

def save_db(db):
    with open(CERT_DB_PATH, "w") as f:
        json.dump(db, f, indent=4)

def revoke_cert(serial_hex):
    db = load_db()
    db[serial_hex.lower()] = "revoked"
    save_db(db)
    print(f"🔴 Certificate {serial_hex} marked as REVOKED.")

def unrevoke_cert(serial_hex):
    db = load_db()
    if serial_hex.lower() in db:
        db[serial_hex.lower()] = "good"
        save_db(db)
        print(f"🟢 Certificate {serial_hex} restored to GOOD.")
    else:
        print(f"⚠️ Serial {serial_hex} not found in DB.")

def run_revoke_cli():
    print("🔧 Certificate Revocation CLI")
    print("Usage: revoke <serial> | unrevoke <serial>")
    cmd = input("> ").strip().split()
    if len(cmd) != 2:
        print("❌ Invalid command")
        return

    action, serial = cmd
    if action == "revoke":
        revoke_cert(serial)
    elif action == "unrevoke":
        unrevoke_cert(serial)
    else:
        print("❌ Unknown command")

