import hashlib
import json
import os
import stat
import time

def generate_invoice():
    timestamp = time.time_ns()
    invoice_id = f"RD-INV-{int(time.time())}"
    
    invoice_data = {
        "corporate_entity": "RobDoe Pty Ltd",
        "abn_framework": "Australian Registered Pty Ltd",
        "invoice_number": invoice_id,
        "timestamp_ns": timestamp,
        "client": "External Commercial Client",
        "line_items": [
            {
                "description": "Custom Workflow Automation & Local Script Deployment",
                "scope": "Phase 1 Execution & Architecture Setup",
                "amount_aud": 1500.00
            }
        ],
        "payment_terms": "50% Upfront Deposit Required ($750.00 AUD equivalent)",
        "payment_rails": {
            "fiat_australia": {
                "method": "OSKO / PayID / Bank Transfer",
                "entity": "RobDoe Pty Ltd",
                "deposit_required_aud": 750.00
            },
            "crypto_settlement": {
                "accepted_assets": ["USDT (ERC-20 / TRC-20)", "USDC", "SOL"],
                "deposit_required_usd_equivalent": 500.00,
                "note": "Wallet routing address provided upon client confirmation."
            }
        },
        "status": "AWAITING_DEPOSIT_SELECTION"
    }

    invoice_hash = hashlib.sha256(json.dumps(invoice_data, sort_keys=True).encode("utf-8")).hexdigest()
    invoice_data["invoice_integrity_hash"] = f"0x{invoice_hash}"

    output_file = f"{invoice_id}_dual_rail.json"
    
    with open(output_file, "w") as f:
        json.dump(invoice_data, f, indent=4)
        
    os.chmod(output_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    print("\n==========================================================")
    print("        DUAL-RAIL COMMERCIAL INVOICE GENERATED            ")
    print("==========================================================")
    print(f"[+] Invoice ID          : {invoice_id}")
    print(f"[+] Fiat Rail           : OSKO / PayID ($750.00 AUD)")
    print(f"[+] Crypto Rail         : USDT / USDC / SOL Enabled")
    print(f"[+] Integrity Hash      : 0x{invoice_hash[:16]}...")
    print(f"[+] Output File         : {output_file}")
    print("[+] Status              : READY FOR DUAL-RAIL DEPLOYMENT")
    print("==========================================================\n")

if __name__ == "__main__":
    generate_invoice()
