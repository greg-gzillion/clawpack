#!/usr/bin/env python3
\"\"\"Mathematicaclaw - Main Entry Point\"\"\"

import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import MathematicaclawCore

def print_welcome():
    print("\n" + "="*70)
    print("MATHEMATICACLAW - Mathematical Computing Agent")
    print("="*70)
    print("\nDISCLAIMER: For educational purposes only.")
    print("This agent shares calculations with other Clawpack agents!")
    print("="*70)
    print("\nCOMMANDS:")
    print("  /calc [expr]      - Calculate expression (e.g., /calc 2+2)")
    print("  /solve [eq]       - Solve equation (e.g., /solve x^2-4=0)")
    print("  /derive [expr]    - Derivative (e.g., /derive x^2)")
    print("  /integrate [expr] - Integral (e.g., /integrate x^2)")
    print("  /limit [expr]     - Limit (e.g., /limit 1/x as x->0)")
    print("  /stats [numbers]  - Statistics (e.g., /stats 1,2,3,4,5)")
    print("  /plot [expr]      - Plot function (e.g., /plot x**2)")
    print("  /plots            - List saved plots")
    print("  /plots clear      - Delete all saved plots")
    print("  /open [name]      - Open a saved plot")
    print("  /help, /quit")
    print("="*70)

def main():
    m = MathematicaclawCore()
    print_welcome()

    while True:
        try:
            cmd = input("\nMathematicaclaw> ").strip()
            if not cmd:
                continue
            
            if cmd == "/quit":
                print("Goodbye!")
                break
            elif cmd == "/help":
                print_welcome()
            elif cmd.startswith("/calc "):
                expr = cmd[6:]
                result = m.calculate(expr)
                if result.get("success"):
                    print(f"Result: {result['result']}")
                else:
                    print(f"Error: {result.get('error')}")
            elif cmd.startswith("/solve "):
                eq = cmd[7:]
                result = m.solve(eq)
                if "solution" in result:
                    print(f"Solution: {result['solution']}")
                else:
                    print(f"Error: {result.get('error')}")
            elif cmd.startswith("/derive "):
                expr = cmd[8:]
                result = m.derivative(expr)
                if "derivative" in result:
                    print(f"Derivative: {result['derivative']}")
                else:
                    print(f"Error: {result.get('error')}")
            elif cmd.startswith("/integrate "):
                expr = cmd[11:]
                result = m.integrate(expr)
                if "result" in result:
                    print(f"Integral: {result['result']}")
                else:
                    print(f"Error: {result.get('error')}")
            elif cmd.startswith("/limit "):
                expr = cmd[7:]
                point = 0
                if " as x->" in expr:
                    parts = expr.split(" as x->")
                    expr = parts[0]
                    point = float(parts[1])
                result = m.limit(expr, point)
                if "result" in result:
                    print(f"Limit: {result['result']}")
                else:
                    print(f"Error: {result.get('error')}")
            elif cmd.startswith("/stats "):
                nums = cmd[7:]
                result = m.statistics(nums)
                if result.get("success"):
                    print(f"Count: {result['count']}, Sum: {result['sum']}, Mean: {result['mean']}")
                else:
                    print(f"Error: {result.get('error')}")
            elif cmd.startswith("/plot "):
                expr = cmd[6:]
                if ";" in expr:
                    expressions = [e.strip() for e in expr.split(";")]
                    result = m.plot_multiple(expressions)
                else:
                    range_match = re.search(r'from\s+([-\d.]+)\s+to\s+([-\d.]+)', expr)
                    if range_match:
                        x_min = float(range_match.group(1))
                        x_max = float(range_match.group(2))
                        expr = expr.replace(range_match.group(0), "").strip()
                        result = m.plot_function(expr, (x_min, x_max))
                    else:
                        result = m.plot_function(expr)
                
                if isinstance(result, str) and result.endswith('.png'):
                    print(f"Plot saved to: {result}")
                    print(f"Location: {os.path.dirname(result)}")
                elif isinstance(result, dict) and "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Plot saved: {result}")
            elif cmd == "/plots":
                plots = m.list_plots()
                if plots:
                    print(f"\nSaved plots ({len(plots)}):")
                    for p in plots:
                        print(f"  {p['name']} - {p['size_kb']} KB")
                    print(f"\nLocation: {m.plots_dir}")
                else:
                    print("No plots saved yet. Use /plot to create one.")
            elif cmd == "/plots clear":
                result = m.clear_plots()
                print(f"Cleared {result['deleted']} plot files")
            elif cmd.startswith("/open "):
                plot_name = cmd[6:]
                plots = m.list_plots()
                for p in plots:
                    if plot_name in p['name']:
                        os.startfile(p['path'])
                        print(f"Opening: {p['name']}")
                        break
                else:
                    print(f"Plot '{plot_name}' not found")
            else:
                print("Unknown command. Try /help")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()