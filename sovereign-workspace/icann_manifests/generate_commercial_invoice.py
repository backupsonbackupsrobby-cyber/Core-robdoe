import hashlib
import json
import os
import stat
import time

def generate_invoice():
    timestamp = time.time_ns()
    invoice_id = f"RD-INV-{int(time.time())}"
    
    # Commercial Service Spec (Lane 1: B2B Automation / Custom Scripting)
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
        "payment_terms": "50% Upfront Deposit Required ($750.00 AUD) via OSKO/PayID",
        "status": "AWAITING_DEPOSIT"
    }

    # Cryptographic integrity stamp for the invoice
    invoice_hash = hashlib.sha256(json.dumps(invoice_data, sort_keys=True).encode("utf-8")).hexdigest()
    invoice_data["invoice_integrity_hash"] = f"0x{invoice_hash}"

    output_file = f"{invoice_id}.json"
    
    with open(output_file, "w") as f:
        json.dump(invoice_data, f, indent=4)
        
    # Lock permissions read-only for immutability
    os.chmod(output_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    print("\n==========================================================")
    print("          COMMERCIAL INVOICE AUTOMATION COMPLETE          ")
    print("==========================================================")
    print(f"[+] Invoice ID          : {invoice_id}")
    print(f"[+] Corporate Entity    : RobDoe Pty Ltd")
    print(f"[+] Total Scope Value   : $1,500.00 AUD")
    print(f"[+] Upfront Deposit Due : $750.00 AUD (50%)")
    print(f"[+] Integrity Hash      : 0x{invoice_hash[:16]}...")
    print(f"[+] Output File         : {output_file}")
    print("[+] Status              : READY FOR CLIENT TRANSMISSION")
    print("==========================================================\n")

if __name__ == "__main__":
    generate_invoice()
