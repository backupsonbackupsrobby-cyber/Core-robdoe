import os
import json
import time

def setup_funding():
    timestamp = time.time_ns()
    
    # Ensure .github directory exists for GitHub native integrations
    github_dir = ".github"
    os.makedirs(github_dir, exist_ok=True)
    
    funding_yaml_content = f"""# RobDoe Pty Ltd / AiAgency101 - Micro-Sponsorship & Support Manifest
# Generated via Termux Automation Pipeline
# Timestamp: {timestamp}

github: [robdoe, AiAgency101]
custom:
  - "https://buymeacoffee.com/robdoe"
  - "https://ko-fi.com/robdoe"
"""

    funding_file = os.path.join(github_dir, "FUNDING.yml")
    with open(funding_file, "w") as f:
        f.write(funding_yaml_content)

    # Also generate a local JSON record for the master grid ledger
    ledger_record = {
        "entity": "RobDoe Pty Ltd",
        "micro_tipping_configured": True,
        "handles": {
            "github_namespaces": ["robdoe", "AiAgency101", "backupsonbackupsrobby-cyber", "LadbotOneLad"],
            "support_links": [
                "https://buymeacoffee.com/robdoe",
                "https://ko-fi.com/robdoe"
            ]
        },
        "timestamp_ns": timestamp
    }

    with open("micro_sponsorship_registry.json", "w") as f:
        json.dump(ledger_record, f, indent=4)

    print("\n==========================================================")
    print("        MICRO-SPONSORSHIP CONFIGURATION COMPLETE          ")
    print("==========================================================")
    print(f"[+] GitHub Funding File : {funding_file}")
    print(f"[+] Local Registry      : micro_sponsorship_registry.json")
    print(f"[+] Support Endpoint    : Buy Me a Coffee / Ko-fi / GitHub Sponsors")
    print("[+] Status              : READY TO PUSH TO REPO")
    print("==========================================================\n")

if __name__ == "__main__":
    setup_funding()
