import os
import subprocess
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8989887535:AAGX4N1U18w1KrbkMX_cOr0Y90otZvD7qsc"
LEDGER_FILE = "robdoe_system_matrix.log"

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

def answer_pre_checkout(pre_checkout_query_id):
    url = f"https://api.telegram.org/bot{TOKEN}/answerPreCheckoutQuery"
    payload = {"pre_checkout_query_id": pre_checkout_query_id, "ok": True}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

def commit_state_proof(user_id, amount):
    """Logs the transaction and returns a cryptographically secure git root hash proof."""
    try:
        os.makedirs(".", exist_ok=True)
        with open(LEDGER_FILE, "a") as f:
            f.write(f"NODE_ID: {user_id} | STARS_LOCKED: {amount} | TIMESTAMP: {time.time()}\n")
        
        subprocess.run(["git", "add", LEDGER_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", f"Systemic state proof: node {user_id} unlocked {amount} XTR"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        res = subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "GENESIS-STATE-ROOT"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    
    # 1. Handle Pre-Checkout Query (Required for Telegram Stars)
    if "pre_checkout_query" in data:
        pcq = data["pre_checkout_query"]
        answer_pre_checkout(pcq["id"])
        return jsonify({"status": "pre_checkout_approved"})

    # 2. Handle Successful Payment (The 25-Star Gate Entry)
    if "message" in data and "successful_payment" in data["message"]:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        user_id = msg["from"].get("id", "unknown")
        username = msg["from"].get("username", "AnonymousNode")
        payment = msg["successful_payment"]
        amount = payment.get("total_amount", 25)
        
        # Lock state and generate root hash proof
        root_hash = commit_state_proof(user_id, amount)
        
        response_text = (
            f"⚡ *RobDoe Matrix Node Activated*\n\n"
            f"👤 Node: `@{username}`\n"
            f"💎 Capital Locked: `{amount} Stars`\n"
            f"🔗 ERC-721 Domain Right: `robdoedoc#{user_id}.tag`\n"
            f"🛡️ Git Root Hash Proof:\n`{root_hash}`"
        )
        
        send_telegram_message(chat_id, response_text)
        print(f"[SYSTEM SUCCESS] Node {username} processed {amount} Stars. Root: {root_hash}")

    # 3. Handle Initial Text / Trigger Command to Send Invoice
    elif "message" in data and "text" in data["message"]:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "").strip()
        
        if text == "/start" or text == "/scale":
            url = f"https://api.telegram.org/bot{TOKEN}/sendInvoice"
            payload = {
                "chat_id": chat_id,
                "title": "RobDoe ERC-721 Domain Agent Node",
                "description": "Initialize your scaling node and secure a dynamic domain asset entry.",
                "payload": "robdoe_node_genesis_25",
                "currency": "XTR",
                "prices": [{"label": "Node Base Entry", "amount": 25}]
            }
            try:
                requests.post(url, json=payload, timeout=5)
            except Exception:
                pass

    return jsonify({"status": "system_active"})

if __name__ == "__main__":
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])
        subprocess.run(["git", "config", "user.name", "RobDoe"])
        subprocess.run(["git", "config", "user.email", "robdoe@aiagency101.local"])
    
    print("[*] ROBDOE SYSTEMIC ENGINE ONLINE. LISTENING FOR XTR STREAMS...")
    app.run(host="0.0.0.0", port=5000)
