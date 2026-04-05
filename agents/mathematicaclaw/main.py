#!/usr/bin/env python3
"""Mathematicaclaw - Main Entry Point"""

from .core import MathematicaclawCore

def print_welcome():
    print("\n" + "="*70)
    print("🧮 MATHEMATICACLAW - Mathematical Computing Agent")
    print("="*70)
    print("\n⚠️ DISCLAIMER: For educational purposes only.")
    print("💡 This agent shares calculations with other Clawpack agents!")
    print("="*70)
    print("\n📚 COMMANDS:")
    print("  /calc [expr]      - Calculate expression")
    print("  /solve [eq]       - Solve equation")
    print("  /derive [expr]    - Derivative")
    print("  /integrate [expr] - Integral")
    print("  /limit [expr]     - Limit")
    print("  /taylor [expr]    - Taylor series")
    print("  /plot [func]      - Plot function")
    print("  /stats [numbers]  - Statistics")
    print("  /help, /quit")
    print("="*70)

def main():
    m = MathematicaclawCore()
    print_welcome()
    
    while True:
        cmd = input("\n🧮 Mathematicaclaw> ").strip()
        if not cmd:
            continue
        if cmd == '/quit':
            break
        if cmd == '/help':
            print_welcome()
            continue
        
        # Calculate
        if cmd.startswith('/calc '):
            result = m.calculate(cmd[6:])
            if result.get("error"):
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Result: {result['value_str']}")
            continue
        
        # Solve
        if cmd.startswith('/solve '):
            result = m.solve(cmd[7:])
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Solution: {result['solution']} (source: {result.get('source', 'unknown')})")
            continue
        
        # Derive
        if cmd.startswith('/derive '):
            result = m.differentiate(cmd[8:])
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Result: {result['derivative']}")
            continue
        
        # Integrate
        if cmd.startswith('/integrate '):
            expr = cmd[11:]
            if " from " in expr:
                parts = expr.split(" from ")
                expr_part = parts[0]
                limits = parts[1].split(" to ")
                a, b = float(limits[0]), float(limits[1])
                result = m.integrate(expr_part, a, b)
            else:
                result = m.integrate(expr)
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Result: {result['result']} (type: {result.get('type', 'indefinite')})")
            continue
        
        # Limit
        if cmd.startswith('/limit '):
            result = m.limit(cmd[7:])
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Limit: {result['result']}")
            continue
        
        # Taylor
        if cmd.startswith('/taylor '):
            result = m.taylor(cmd[8:])
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Series: {result['result']}")
            continue
        
        # Plot
        if cmd.startswith('/plot '):
            result = m.plot(cmd[6:])
            if result.get("error"):
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Plot saved to: {result['path']}")
            continue
        
        # Statistics
        if cmd.startswith('/stats '):
            try:
                data = [float(x.strip()) for x in cmd[7:].split(',')]
                result = m.statistics(data)
                if "error" in result:
                    print(f"❌ Error: {result['error']}")
                else:
                    print(f"✅ Count: {result['count']}, Mean: {result['mean']:.4f}, StdDev: {result['std_dev']:.4f}")
            except Exception as e:
                print(f"❌ Error parsing data: {e}")
            continue
        
        print("Unknown command. Type /help")

if __name__ == "__main__":
    main()