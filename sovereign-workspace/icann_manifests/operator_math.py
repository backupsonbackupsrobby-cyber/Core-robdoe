import math

def scaling_operator(initial_state: float, target_state: float, growth_factor: float) -> int:
    """
    Computes pure exponential expansion: 
    State_n = Initial * (Factor)^n
    Solving for n (iterations): n = log(Target / Initial) / log(Factor)
    """
    if initial_state <= 0 or target_state <= initial_state:
        return 0
    
    iterations = math.log(target_state / initial_state) / math.log(growth_factor)
    return math.ceil(iterations)

if __name__ == "__main__":
    initial = 25.0
    target = 1_000_000.0
    
    # Example 1: Aggressive viral multiplier (Each node spawns/converts 4 sub-nodes)
    factor_viral = 4.0
    steps_viral = scaling_operator(initial, target, factor_viral)
    
    # Example 2: Compounding asset yield operator (1.5x recursive growth per cycle)
    factor_yield = 1.5
    steps_yield = scaling_operator(initial, target, factor_yield)

    print(f"[*] Initial Matrix State: {initial}")
    print(f"[*] Target Matrix State:  {target:,}")
    print("-" * 50)
    print(f"[+] Operator [Factor 4.0x Viral Loop]: Requires {steps_viral} recursive cycles.")
    print(f"[+] Operator [Factor 1.5x Yield Loop]: Requires {steps_yield} recursive cycles.")
    
    # Mathematical proof validation loop
    current = initial
    print("\n[⚡] Executing Pure-Math 4.0x Geometric Progression:")
    for i in range(1, steps_viral + 1):
        current *= factor_viral
        print(f"    Cycle {i}: State Value = {current:,.2f}")
