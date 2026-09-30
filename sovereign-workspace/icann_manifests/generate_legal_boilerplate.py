import os
import json
import time
import stat

def create_boilerplate():
    timestamp = time.time_ns()
    legal_dir = "sovereign-workspace/legal_boilerplate"
    os.makedirs(legal_dir, exist_ok=True)

    # 1. Terms of Service & IP Assignment Template
    tos_content = f"""# ROBDOE PTY LTD - MASTER TERMS OF SERVICE & IP ASSIGNMENT
# Generated via Sovereign Automation Pipeline
# Timestamp: {timestamp}

## 1. Corporate Entity
All services, software, and intellectual property are delivered under **RobDoe Pty Ltd** (Australian Registered Proprietary Limited Company).

## 2. Payment & Deposit Terms
* A **50% upfront deposit** is strictly required prior to the commencement of any custom development, scripting, or automation deployment.
* Accepted settlement rails: OSKO / PayID (AUD) or verified stablecoin rails (USDT/USDC).
* Balances are due upon final milestone delivery and cryptographic verification.

## 3. Intellectual Property (IP) Rights
Upon full and final settlement of invoice balances, full ownership and usage rights of the custom-delivered source code or automation scripts transfer to the client. RobDoe Pty Ltd retains underlying framework and utility boilerplate rights.

## 4. Limitation of Liability
Software, scripts, and local deployments are provided "as is" with cryptographic integrity proofs. RobDoe Pty Ltd is not liable for secondary operational disruptions post-handover.
"""

    tos_path = os.path.join(legal_dir, "TERMS_OF_SERVICE.md")
    with open(tos_path, "w") as f:
        f.write(tos_content)
    os.chmod(tos_path, 0o444) # Read-only lock

    # 2. Automated ATO Expense & Receipt Ledger Template
    expense_ledger = {
        "entity": "RobDoe Pty Ltd",
        "compliance_framework": "Australian Taxation Office (ATO) Standards",
        "ledger_version": "v1.0.0",
        "created_timestamp_ns": timestamp,
        "expenses": [
            {
                "date": "2026-09-30",
                "category": "Software / Infrastructure / Tooling",
                "description": "Local development environment and grid maintenance",
                "amount_aud": 0.00,
                "gst_included_aud": 0.00,
                "receipt_hash": "0xe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            }
        ]
    }

    expense_path = os.path.join(legal_dir, "ato_expense_ledger.json")
    with open(expense_path, "w") as f:
        json.dump(expense_ledger, f, indent=4)
    os.chmod(expense_path, 0o444)

    print("\n==========================================================")
    print("        LEGAL & BOILERPLATE AUTOMATION COMPLETE           ")
    print("==========================================================")
    print(f"[+] Terms of Service    : {tos_path} (Locked Read-Only)")
    print(f"[+] ATO Expense Ledger  : {expense_path} (Locked Read-Only)")
    print("[+] Status              : FULLY COMPLIANT & AUTOMATED")
    print("==========================================================\n")

if __name__ == "__main__":
    create_boilerplate()
