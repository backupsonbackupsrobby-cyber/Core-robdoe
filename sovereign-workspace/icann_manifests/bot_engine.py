import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration
TOKEN = "8989887535:AAGX4N1U18w1KrbkMX_cOr0Y90otZvD7qsc"
LEDGER_FILE = "scaling_ledger.txt"

def get_git_root_hash():
    """Extracts the latest git commit hash as a verifiable state proof."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "No local git commit found yet."

def log_transaction(user_id, amount):
    """Logs the incoming 25-Star entry and commits it to git."""
    os.makedirs("data", exist_ok=True)
    with open(LEDGER_FILE, "a") as f:
        f.write(f"User: {user_id} | Stars: {amount} | Status: Active Scaling Node\n")
    
    # Auto-commit state change to get the new root hash
    subprocess.run(["git", "add", LEDGER_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", f"Auto-state proof for node {user_id}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    
    # Check if user sent a successful payment (Telegram Stars use currency 'XTR')
    if "message" in data and "successful_payment" in data["message"]:
        payment = data["message"]["successful_payment"]
        user_id = data["message"]["from"]["id"]
        amount = payment.get("total_amount", 25) # Default to 25 Stars target gate
        
        # Log and hash
        log_transaction(user_id, amount)
        root_hash = get_git_root_hash()
        
        print(f"[+] Scaling Node Triggered! User: {user_id} | Stars: {amount}")
        print(f"[+] Current Git Root Hash Proof: {root_hash}")
        
        # Here you would typically use requests to send a Telegram message back to the user 
        # with their ERC-721 domain assignment and root hash receipt.
        
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Ensure local git repo is initialized
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])
        subprocess.run(["git", "config", "user.name", "RobDoe"])
        subprocess.run(["git", "config", "user.email", "robdoe@local.bot"])
    
    print("[*] Termux Scaling Bot Engine running on port 5000...")
    app.run(host="0.0.0.0", port=5000)
