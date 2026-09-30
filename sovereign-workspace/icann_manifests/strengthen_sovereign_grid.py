import hashlib
import json
import os
import stat
import time

def strengthen_grid():
    timestamp = time.time_ns()
    workspace_dir = "sovereign-workspace/icann_manifests"
    
    if not os.path.exists(workspace_dir):
        print(f"[-] Workspace not found at {workspace_dir}. Creating it now...")
        os.makedirs(workspace_dir, exist_ok=True)

    os.chdir(workspace_dir)
    
    # Audit all json files in the workspace
    manifests = [f for f in os.listdir(".") if f.endswith(".json")]
    
    audit_ledger = {
        "audit_timestamp_ns": timestamp,
        "audited_files": [],
        "master_hardening_hash": ""
    }

    combined_hash_input = ""
    for filename in sorted(manifests):
        # Lock file permissions to read-only for security (chmod 444 equivalent in python)
        os.chmod(filename, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        
        with open(filename, "r") as f:
            content = f.read()
            file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            
        audit_ledger["audited_files"].append({
            "file": filename,
            "sha256": f"0x{file_hash}",
            "status": "HARDENED_READ_ONLY"
        })
        combined_hash_input += file_hash

    # Generate master grid defense hash
    master_defense_hash = hashlib.sha256(combined_hash_input.encode("utf-8")).hexdigest()
    audit_ledger["master_hardening_hash"] = f"0x{master_defense_hash}"

    with open("sovereign_grid_audit_proof.json", "w") as f:
        # Temporarily make writable to write report, then lock
        os.chmod("sovereign_grid_audit_proof.json", stat.S_IWRITE | stat.S_IREAD)
        json.dump(audit_ledger, f, indent=4)
        os.chmod("sovereign_grid_audit_proof.json", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    print("\n==========================================================")
    print("          GRID HARDENING & INTEGRITY LOCK COMPLETE        ")
    print("==========================================================")
    print(f"[+] Files Audited & Locked : {len(manifests)}")
    print(f"[+] Master Defense Hash    : 0x{master_defense_hash[:16]}...")
    print(f"[+] Verification Ledger    : sovereign_grid_audit_proof.json")
    print("[+] Status                 : IMMUTABLE DISK STATE ENFORCED")
    print("==========================================================\n")

if __name__ == "__main__":
    strengthen_grid()
