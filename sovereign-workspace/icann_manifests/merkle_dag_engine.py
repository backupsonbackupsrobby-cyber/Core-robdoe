import hashlib
import json
import os

class MerkleDAGNode:
    def __init__(self, data: str, children: list = None):
        self.data = data
        self.children = children if children else []
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Pure math content-addressing: SHA-256 over data + sorted child hashes."""
        hasher = hashlib.sha256()
        hasher.update(self.data.encode('utf-8'))
        for child in sorted(self.children, key=lambda c: c.hash):
            hasher.update(child.hash.encode('utf-8'))
        return hasher.hexdigest()

    def to_dict(self):
        return {
            "hash": self.hash,
            "data": self.data,
            "children": [child.to_dict() for child in self.children]
        }

class SelfSufficientDAG:
    def __init__(self, store_file="dag_store.json"):
        self.store_file = store_file
        self.nodes = {}

    def add_node(self, data: str, child_hashes: list = None) -> MerkleDAGNode:
        """Constructs a new self-sufficient node using existing child references."""
        resolved_children = [self.nodes[ch] for ch in child_hashes if ch in self.nodes]
        node = MerkleDAGNode(data, resolved_children)
        self.nodes[node.hash] = node
        self.save_state()
        return node

    def verify_integrity(self, node_hash: str) -> bool:
        """Pure math verification of node lineage and immutable structural proof."""
        if node_hash not in self.nodes:
            return False
        node = self.nodes[node_hash]
        recomputed = node._compute_hash()
        if node.hash != recomputed:
            return False
        return all(self.verify_integrity(c.hash) for c in node.children)

    def save_state(self):
        data = {h: node.to_dict() for h, node in self.nodes.items()}
        with open(self.store_file, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    print("[*] Initializing Pure-Math Self-Sufficient Merkle DAG Engine...")
    dag = SelfSufficientDAG()

    # 1. Create independent base leaves (Genesis Nodes)
    leaf1 = dag.add_node("RobDoe_Node_Alpha_25_XTR")
    leaf2 = dag.add_node("RobDoe_Node_Beta_Domain_State")
    
    print(f"[+] Leaf 1 Hash: {leaf1.hash}")
    print(f"[+] Leaf 2 Hash: {leaf2.hash}")

    # 2. Build parent node mathematically merging children
    root = dag.add_node("RobDoe_Root_Consensus_Matrix", [leaf1.hash, leaf2.hash])
    print(f"[⚡] Merkle DAG Root Hash: {root.hash}")

    # 3. Verify math integrity
    is_valid = dag.verify_integrity(root.hash)
    print(f"[🛡️] DAG Self-Verification Status: {'PASSED (Immutable)' if is_valid else 'FAILED'}")
