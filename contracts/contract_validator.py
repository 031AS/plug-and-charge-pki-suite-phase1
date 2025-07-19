# contracts/contract_validator.py
import json
import os

CONTRACTS_PATH = "contracts/contracts.json"

def load_contracts():
    if not os.path.exists(CONTRACTS_PATH):
        return {}
    with open(CONTRACTS_PATH, "r") as f:
        return json.load(f)

def validate_contract(emaid):
    contracts = load_contracts()
    status = contracts.get(emaid)
    if status == "valid":
        print(f"✅ Contract for EMAID {emaid} is valid.")
        return True
    else:
        print(f"❌ No valid contract found for EMAID {emaid}")
        return False

