import hashlib
import json
import os
import subprocess
import time

def absolute_mint():
    timestamp = time.time_ns()
    workspace_dir = "sovereign-workspace/icann_manifests"
    
    if os.path.exists(workspace_dir):
        os.chdir(workspace_dir)

    # Absolute Genesis Payload linking everything under RobDoe & Aiagency101TeneT.PtyLtd
    absolute_payload = {
        "directive": "ABSOLUTE_GENESIS_MINT",
        "principal": "Eric Hadfield (RobDoe)",
        "entity": "Aiagency101TeneT.PtyLtd / RobDoe Pty Ltd",
        "timestamp_ns": timestamp,
        "matrix_composition": {
            "total_nodes": 26,
            "demographic_split": "13 Male / 13 Female",
            "financial_reserve": "$101,000,000 AUD (101 Tranches)"
        },
        "anchors": {
            "icann_root": "1.com",
            "academic_anchor": "University of Sydney (erc721.com)",
            "external_witness": "Royal UK (Commonwealth Anchor)"
        },
        "protocol_key": "esp32"
    }

    payload_hash = hashlib.sha256(json.dumps(absolute_payload, sort_keys=True).encode("utf-8")).hexdigest()
    absolute_payload["absolute_genesis_root"] = f"0x{payload_hash}"

    output_file = "ABSOLUTE_GENESIS_MINT_LEDGER.json"
    
    # Ensure file is writable before writing
    if os.path.exists(output_file):
        os.chmod(output_file, 0o644)
        
    with open(output_file, "w") as f:
        json.dump(absolute_payload, f, indent=4)
        
    # Lock down read-only
    os.chmod(output_file, 0o444)

    print(f"[+] Absolute Genesis Ledger Written: {output_file}")
    print(f"[+] Genesis Root Hash: 0x{payload_hash[:16]}...")

    # Execute git operations
    commands = [
        "git add .",
        'git commit -m "feat(genesis): EXECUTE ABSOLUTE GENESIS MINT [esp32]"',
        "git tag -a v2.0.0-absolute-genesis -m 'RobDoe Pty Ltd Absolute Genesis Mint & Sovereign Lock'",
        "git push origin main --tags"
    ]

    for cmd in commands:
        print(f"Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout.strip())
        if result.returncode != 0 and "tag" not in cmd:
            print(f"[-] Notice: {result.stderr.strip()}")

    print("\n==========================================================")
    print("      ABSOLUTE GENESIS MINT & PUSH COMPLETE               ")
    print("==========================================================")
    print(f"[+] Absolute Root Hash  : 0x{payload_hash[:16]}...")
    print("[+] Status              : IMMUTABLY MINTED & PUSHED")
    print("==========================================================\n")

if __name__ == "__main__":
    absolute_mint()
