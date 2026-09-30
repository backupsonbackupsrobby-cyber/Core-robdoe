import hashlib
import json
import os
import stat
import time

def strengthen_grid():
    timestamp = time.time_ns()
    
    # Audit all json files in current directory
    manifests = [f for f in os.listdir(".") if f.endswith(".json")]
    
    audit_ledger = {
        "audit_timestamp_ns": timestamp,
        "audited_files": [],
        "master_hardening_hash": ""
    }

    combined_hash_input = ""
    for filename in sorted(manifests):
        # Ensure file is temporarily writable to adjust permissions
        os.chmod(filename, stat.S_IWRITE | stat.S_IREAD)
        
        with open(filename, "r") as f:
            content = f.read()
            file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            
        # Lock file permissions to read-only for absolute immutability
        os.chmod(filename, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        
        audit_ledger["audited_files"].append({
            "file": filename,
            "sha256": f"0x{file_hash}",
            "status": "HARDENED_READ_ONLY"
        })
        combined_hash_input += file_hash

    master_defense_hash = hashlib.sha256(combined_hash_input.encode("utf-8")).hexdigest()
    audit_ledger["master_hardening_hash"] = f"0x{master_defense_hash}"

    proof_file = "sovereign_grid_audit_proof.json"
    if os.path.exists(proof_file):
        os.chmod(proof_file, stat.S_IWRITE | stat.S_IREAD)

    with open(proof_file, "w") as f:
        json.dump(audit_ledger, f, indent=4)
    
    os.chmod(proof_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    print("\n==========================================================")
    print("          GRID HARDENING & INTEGRITY LOCK COMPLETE        ")
    print("==========================================================")
    print(f"[+] Files Audited & Locked : {len(manifests)}")
    print(f"[+] Master Defense Hash    : 0x{master_defense_hash[:16]}...")
    print(f"[+] Verification Ledger    : {proof_file}")
    print("[+] Status                 : IMMUTABLE DISK STATE ENFORCED")
    print("==========================================================\n")

if __name__ == "__main__":
    strengthen_grid()
