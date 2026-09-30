import time
import hashlib
import json
import os

class LockedMerkleNode:
    def __init__(self, step: int, value: float, z_state: float, duration_ns: int, parent_hash: str = "GENESIS"):
        self.step = step
        self.value = value
        self.z_state = z_state
        self.duration_ns = duration_ns
        self.parent_hash = parent_hash
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = f"{self.step}|{self.value}|{self.z_state}|{self.duration_ns}|{self.parent_hash}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def execute_locked_fractal_engine(c_real: float = 0.314, target: float = 1_000_000.0):
    print(f"[*] Locking Fractal-DAG Engine | Target: {target:,.2f} | Constant C: {c_real}")
    print("-" * 75)
    
    z = 0.0
    scale_accumulator = 25.0
    previous_hash = "GENESIS_ROOT_25_STARS"
    
    chain = []
    total_start_time = time.perf_counter_ns()
    
    i = 0
    while scale_accumulator < target:
        i += 1
        iteration_start = time.perf_counter_ns()
        
        # Core Mandelbrot feedback math: Z = z^2 + c
        z = (z * z) + c_real
        scale_accumulator *= (abs(z) + 1.15)
        
        iteration_end = time.perf_counter_ns()
        duration_ns = iteration_end - iteration_start
        
        # Lock state into immutable Merkle node
        node = LockedMerkleNode(
            step=i,
            value=scale_accumulator,
            z_state=z,
            duration_ns=duration_ns,
            parent_hash=previous_hash
        )
        previous_hash = node.hash
        chain.append(node)
        
        print(f"    Step {i:2d} | Z: {z:8.4f} | Value: {scale_accumulator:14,.2f} | Time: {duration_ns/1_000:8.2f} µs | Hash: {node.hash[:12]}...")

    total_end_time = time.perf_counter_ns()
    total_duration_ms = (total_end_time - total_start_time) / 1_000_000
    
    print("-" * 75)
    print(f"[⚡] TARGET LOCKED & BREACHED IN STEP {i}!")
    print(f"[🛡️] Final Terminal Value: {scale_accumulator:,.2f}")
    print(f"[⏱️] Total Execution Time: {total_duration_ms:.4f} ms")
    print(f"[🔒] Immutable Final Merkle Root Proof:\n     {previous_hash}")
    
    # Save ledger proof locally
    proof_data = {
        "target": target,
        "total_steps": i,
        "final_value": scale_accumulator,
        "total_duration_ms": total_duration_ms,
        "merkle_root": previous_hash
    }
    with open("fractal_lock_proof.json", "w") as f:
        json.dump(proof_data, f, indent=2)
    print(f"[💾] Proof locked to 'fractal_lock_proof.json'")

if __name__ == "__main__":
    execute_locked_fractal_engine()
