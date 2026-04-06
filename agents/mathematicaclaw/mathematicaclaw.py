#!/usr/bin/env python3
"""Simple Mathematicaclaw - Working Version"""

import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
# Shared memory integration
import sqlite3
from pathlib import Path

def save_to_shared_memory(expression, result, operation):
    try:
        db_path = Path.home() / ".claw_memory" / "shared_memory.db"
        conn = sqlite3.connect(str(db_path))
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS math_knowledge
                     (id INTEGER PRIMARY KEY, expression TEXT UNIQUE, 
                      result TEXT, operation TEXT, timestamp TEXT)''')
        c.execute('INSERT OR REPLACE INTO math_knowledge (expression, result, operation, timestamp) VALUES (?,?,?,?)',
                  (expression, str(result), operation, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

import os

# Create plots directory
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

def calculate(expr):
    try:
        result = sp.sympify(expr)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def solve_eq(eq):
    try:
        if "=" in eq:
            left, right = eq.split("=")
            expr = sp.sympify(left) - sp.sympify(right)
        else:
            expr = sp.sympify(eq)
        x = sp.Symbol("x")
        solutions = sp.solve(expr, x)
        return str(solutions)
    except Exception as e:
        return f"Error: {e}"

def derivative(expr):
    try:
        x = sp.Symbol("x")
        f = sp.sympify(expr)
        deriv = sp.diff(f, x)
        return str(deriv)
    except Exception as e:
        return f"Error: {e}"

def integral(expr, a=None, b=None):
    try:
        x = sp.Symbol("x")
        f = sp.sympify(expr)
        if a is not None and b is not None:
            result = sp.integrate(f, (x, a, b))
            return str(result)
        else:
            result = sp.integrate(f, x)
            return str(result) + " + C"
    except Exception as e:
        return f"Error: {e}"

def limit_expr(expr, point):
    try:
        x = sp.Symbol("x")
        f = sp.sympify(expr)
        result = sp.limit(f, x, point)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def statistics(nums):
    try:
        numbers = [float(n.strip()) for n in nums.split(",")]
        count = len(numbers)
        total = sum(numbers)
        mean = total / count
        return f"Count: {count}, Sum: {total}, Mean: {mean}"
    except Exception as e:
        return f"Error: {e}"

def plot_function(expr, x_min=-10, x_max=10):
    try:
        x = sp.Symbol("x")
        f = sp.lambdify(x, sp.sympify(expr), "numpy")
        x_vals = np.linspace(x_min, x_max, 1000)
        y_vals = f(x_vals)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=f"f(x) = {expr}")
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)
        plt.grid(True, alpha=0.3)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title(f"Plot of {expr}")
        plt.legend()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = expr.replace("*", "_").replace("/", "_").replace("^", "_")[:30]
        filename = f"plot_{safe_name}_{timestamp}.png"
        filepath = os.path.join(PLOTS_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        return f"Plot saved to: {filepath}"
    except Exception as e:
        return f"Error: {e}"

def list_plots():
    plots = [f for f in os.listdir(PLOTS_DIR) if f.endswith(".png")]
    if plots:
        result = f"\nSaved plots ({len(plots)}):\n"
        for p in plots:
            size = os.path.getsize(os.path.join(PLOTS_DIR, p)) / 1024
            result += f"  {p} - {size:.1f} KB\n"
        result += f"\nLocation: {PLOTS_DIR}"
        return result
    return "No plots saved yet. Use /plot to create one."

def clear_plots():
    count = 0
    for f in os.listdir(PLOTS_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(PLOTS_DIR, f))
            count += 1
    return f"Cleared {count} plot files"

def print_welcome():
    print("\n" + "="*70)
    print("MATHEMATICACLAW - Mathematical Computing Agent")
    print("="*70)
    print("\nDISCLAIMER: For educational purposes only.")
    print("="*70)
    print("\nCOMMANDS:")
    print("  /calc 2+2              - Calculate expression")
    print("  /solve x^2-4=0         - Solve equation")
    print("  /derive x^2            - Derivative")
    print("  /integrate x^2         - Integral")
    print("  /limit 1/x as x->0     - Limit")
    print("  /stats 1,2,3,4,5       - Statistics")
    print("  /plot x**2             - Plot function")
    print("  /plot x**2 from -5 to 5 - Plot with custom range")
    print("  /plots                 - List saved plots")
    print("  /plots clear           - Delete all plots")
    print("  /help, /quit")
    print("="*70)

def main():
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
                print(f"Result: {calculate(expr)}")
            elif cmd.startswith("/solve "):
                eq = cmd[7:]
                print(f"Solution: {solve_eq(eq)}")
            elif cmd.startswith("/derive "):
                expr = cmd[8:]
                print(f"Derivative: {derivative(expr)}")
            elif cmd.startswith("/integrate "):
                expr = cmd[11:]
                print(f"Integral: {integral(expr)}")
            elif cmd.startswith("/limit "):
                expr = cmd[7:]
                point = 0
                if " as x->" in expr:
                    parts = expr.split(" as x->")
                    expr = parts[0]
                    point = float(parts[1])
                print(f"Limit: {limit_expr(expr, point)}")
            elif cmd.startswith("/stats "):
                nums = cmd[7:]
                print(statistics(nums))
            elif cmd.startswith("/plot "):
                expr = cmd[6:]
                x_min, x_max = -10, 10
                if " from " in expr and " to " in expr:
                    parts = expr.split(" from ")
                    expr = parts[0]
                    range_parts = parts[1].split(" to ")
                    x_min = float(range_parts[0])
                    x_max = float(range_parts[1])
                print(plot_function(expr, x_min, x_max))
            elif cmd == "/plots":
                print(list_plots())
            elif cmd == "/plots clear":
                print(clear_plots())
            else:
                print("Unknown command. Try /help")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
