import math

def fractal_scaling_operator(c_real: float, max_iterations: int = 25) -> float:
    """
    Applies the Mandelbrot recursive feedback engine: Z = z^2 + c
    Tracking magnitude growth over recursive cycles to scale value.
    """
    z = 0.0
    # Scaling factor initialization
    scale_accumulator = 25.0 
    
    print(f"[*] Initializing Fractal Operator | C-Constant: {c_real}")
    
    for i in range(1, max_iterations + 1):
        # Core Mandelbrot complex dynamics mapped to real-line feedback
        z = (z * z) + c_real
        
        # Apply magnitude expansion to our target asset scale
        scale_accumulator *= (abs(z) + 1.15)
        
        print(f"    Iteration {i:2d} | Z-State: {z:10.4f} | Scaled Value: {scale_accumulator:15,.2f}")
        
        if scale_accumulator >= 1_000_000:
            print(f"\n[⚡] TARGET REACHED AT ITERATION {i}: {scale_accumulator:,.2f}")
            return scale_accumulator
            
    return scale_accumulator

if __name__ == "__main__":
    # Using a tuned constant 'c' to drive geometric expansion without immediate divergence blowup
    fractal_scaling_operator(c_real=0.314, max_iterations=15)
