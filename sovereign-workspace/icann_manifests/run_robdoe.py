import os
import subprocess
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8989887535:AAGX4N1U18w1KrbkMX_cOr0Y90otZvD7qsc"
LEDGER = "robdoe_scaling_matrix.log"

def commit_and_hash():
    try:
        subprocess.run(["git", "add", LEDGER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", "RobDoe Autonomous Scaling Node Push"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        res = subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "GENESIS-HASH"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        msg = data["message"]
        user = msg.get("from", {}).get("username", "UnknownNode")
        text = msg.get("text", "")
        
        os.makedirs(".", exist_ok=True)
        with open(LEDGER, "a") as f:
            f.write(f"NODE: {user} | MSG: {text} | TIME: {time.time()}\n")
        
        root_hash = commit_and_hash()
        print(f"[ROBDOE ENGINE] Node Activated: {user} | Root Proof: {root_hash}")
        
    return jsonify({"status": "active", "matrix": "robdoe"})

if __name__ == "__main__":
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])
        subprocess.run(["git", "config", "user.name", "RobDoe"])
        subprocess.run(["git", "config", "user.email", "robdoe@aiagency101.local"])
    
    print("[+] ROBDOE UNSTOPPABLE ENGINE ONLINE ON PORT 5000...")
    app.run(host="0.0.0.0", port=5000)
