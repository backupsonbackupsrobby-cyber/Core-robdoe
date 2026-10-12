cat << 'EOF' > wallet.py
#!/usr/bin/env python3
import urllib.request
import json
import hashlib
import time

ACCOUNTS = {
    "Solana": "3sZ2G9spssmLMZDMcZF5FMca4udBWNQkGLiaeBEzUPHn",
}

def query_solana_balance(address):
    try:
        url = "https://api.mainnet-beta.solana.com"
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [address]
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url, 
            data=payload, 
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            res = json.loads(response.read().decode())
            lamports = res.get("result", {}).get("value", 0)
            return lamports / 1e9
    except Exception:
        return 0.0

def generate_merkle_root(data_dict):
    leaves = [hashlib.sha256(f"{k}:{v}".encode()).hexdigest() for k, v in data_dict.items()]
    if not leaves:
        return hashlib.sha256(b"empty").hexdigest()
    
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i+1 < len(current_level) else left
            parent = hashlib.sha256((left + right).encode()).hexdigest()
            next_level.append(parent)
        current_level = next_level
    return current_level[0]

def main():
    print("=" * 60)
    print(" ⚡ TERMINAL LIQUIDITY VERIFIER & STATE ENGINE")
    print("=" * 60)
    
    balances = {}
    for chain, addr in ACCOUNTS.items():
        print(f"[*] Querying {chain} node for `{addr[:8]}...`")
        bal = query_solana_balance(addr) if chain == "Solana" else 0.0
        balances[chain] = bal
        print(f"    -> Balance: {bal:.4f} {chain}")

    merkle_root = generate_merkle_root(balances)
    
    print("-" * 60)
    print(f" Timestamp : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" State Root: {merkle_root}")
    print("=" * 60)

if __name__ == "__main__":
    main()
EOF
[?2004h[?1049h[22;0;0t[1;34r(B[m[4l[?7h[39;49m[?1h=[?1h=[?25l[39;49m(B[m[H[2J[32;27H(B[0;7m[ New File ](B[m[?12l[?25h[34;1H[?1049l[23;0;0t[?1l>[?2004l
