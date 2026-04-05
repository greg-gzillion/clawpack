#!/usr/bin/env python3
# mathematicaclaw_shared.py - Mathematical Computing Agent

import requests
import sqlite3
import math
import cmath
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import plotting libraries
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

# Import symbolic math
try:
    import sympy as sp
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False
    print("⚠️ SymPy not installed. Install with: pip install sympy")

CLOUD_API_KEY = "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"


class SharedMemory:
    def __init__(self):
        self.path = Path.home() / ".claw_memory" / "shared_memory.db"
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(str(self.path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS math_knowledge (
                expression TEXT,
                result TEXT,
                operation TEXT,
                timestamp TEXT,
                PRIMARY KEY (expression, operation)
            )
        """)
        conn.commit()
        conn.close()
    
    def get(self, expr: str, op: str) -> Optional[str]:
        conn = sqlite3.connect(str(self.path))
        cur = conn.execute("SELECT result FROM math_knowledge WHERE expression = ? AND operation = ?", (expr, op))
        row = cur.fetchone()
        conn.close()
        if row:
            print("📚 [FROM SHARED MEMORY]")
            return row[0]
        return None
    
    def set(self, expr: str, result: str, op: str):
        conn = sqlite3.connect(str(self.path))
        conn.execute("INSERT OR REPLACE INTO math_knowledge VALUES (?, ?, ?, ?)",
                     (expr, result, op, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        print("💡 [SAVED TO SHARED MEMORY]")


class Mathematicaclaw:
    def __init__(self):
        self.name = "Mathematicaclaw"
        self.memory = SharedMemory()
        self.plot_path = Path.home() / ".claw_memory" / "plots"
        self.plot_path.mkdir(parents=True, exist_ok=True)
        self._print_welcome()
    
    def _print_welcome(self):
        print("\n" + "="*70)
        print("🧮 MATHEMATICACLAW - Mathematical Computing Agent")
        print("="*70)
        print("\n📚 COMMANDS:")
        print("  /calc <expr>      - Calculate (2+2, sin(pi/2))")
        print("  /solve <eq>       - Solve equation (x^2 - 4 = 0)")
        print("  /derive <expr>    - Derivative (x^3)")
        print("  /integrate <expr> - Integral (x^2) or (x^2 from 0 to 2)")
        print("  /limit <expr>     - Limit (sin(x)/x)")
        print("  /taylor <expr>    - Taylor series (sin(x))")
        print("  /plot <func>      - Plot function (sin(x))")
        print("  /stats <nums>     - Statistics (1,2,3,4,5)")
        print("  /help, /quit")
        print("="*70)
    
    def calc(self, expr: str) -> Dict:
        try:
            allowed = dict(math.__dict__)
            allowed.update({"i": 1j, "j": 1j, "pi": math.pi, "e": math.e})
            allowed.update(cmath.__dict__)
            
            result = eval(expr, {"__builtins__": {}}, allowed)
            if isinstance(result, complex):
                val = f"{result.real:.6g}{result.imag:+.6g}j"
            else:
                val = str(result)
            return {"success": True, "result": val}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def solve(self, eq: str) -> Dict:
        if not SYMPY_AVAILABLE:
            return {"success": False, "error": "SymPy not installed"}
        
        cached = self.memory.get(eq, "solve")
        if cached:
            return {"success": True, "result": cached, "source": "shared"}
        
        try:
            x = sp.Symbol('x')
            expr = sp.sympify(eq.replace("=", "-"))
            solutions = sp.solve(expr, x)
            result = str(solutions)
            self.memory.set(eq, result, "solve")
            return {"success": True, "result": result, "source": "sympy"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def derive(self, expr: str) -> Dict:
        if not SYMPY_AVAILABLE:
            return {"success": False, "error": "SymPy not installed"}
        
        cached = self.memory.get(expr, "derive")
        if cached:
            return {"success": True, "result": cached, "source": "shared"}
        
        try:
            x = sp.Symbol('x')
            deriv = sp.diff(sp.sympify(expr), x)
            result = str(sp.simplify(deriv))
            self.memory.set(expr, result, "derive")
            return {"success": True, "result": result, "source": "sympy"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def integrate(self, expr: str, a: float = None, b: float = None) -> Dict:
        if not SYMPY_AVAILABLE:
            return {"success": False, "error": "SymPy not installed"}
        
        key = f"{expr}|{a}|{b}"
        cached = self.memory.get(key, "integrate")
        if cached:
            return {"success": True, "result": cached, "source": "shared"}
        
        try:
            x = sp.Symbol('x')
            if a is not None and b is not None:
                result = sp.integrate(sp.sympify(expr), (x, a, b))
                if isinstance(result, (int, float)):
                    result = f"{float(result):.6f}"
                else:
                    result = str(result)
            else:
                result = str(sp.integrate(sp.sympify(expr), x))
            self.memory.set(key, result, "integrate")
            return {"success": True, "result": result, "source": "sympy"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def limit(self, expr: str) -> Dict:
        if not SYMPY_AVAILABLE:
            return {"success": False, "error": "SymPy not installed"}
        
        cached = self.memory.get(expr, "limit")
        if cached:
            return {"success": True, "result": cached, "source": "shared"}
        
        try:
            x = sp.Symbol('x')
            result = str(sp.limit(sp.sympify(expr), x, 0))
            self.memory.set(expr, result, "limit")
            return {"success": True, "result": result, "source": "sympy"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def taylor(self, expr: str) -> Dict:
        if not SYMPY_AVAILABLE:
            return {"success": False, "error": "SymPy not installed"}
        
        cached = self.memory.get(expr, "taylor")
        if cached:
            return {"success": True, "result": cached, "source": "shared"}
        
        try:
            x = sp.Symbol('x')
            series = sp.series(sp.sympify(expr), x, 0, 5)
            result = str(series)
            self.memory.set(expr, result, "taylor")
            return {"success": True, "result": result, "source": "sympy"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def plot(self, expr: str) -> Dict:
        try:
            expr_fixed = expr.replace('^', '**')
            x_vals = np.linspace(-10, 10, 1000)
            
            def f(x):
                d = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan,
                     "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "e": np.e}
                return eval(expr_fixed, {"__builtins__": {}}, d)
            
            y_vals = [f(x) for x in x_vals]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_vals, y_vals, 'b-', linewidth=2)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            ax.grid(True, alpha=0.3)
            ax.set_title(f'Plot of {expr}')
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = self.plot_path / f"plot_{timestamp}.png"
            plt.savefig(path, dpi=150, bbox_inches='tight')
            plt.close()
            return {"success": True, "path": str(path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def stats(self, data: List[float]) -> Dict:
        if not data:
            return {"success": False, "error": "No data"}
        n = len(data)
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        return {
            "success": True,
            "count": n,
            "sum": sum(data),
            "mean": mean,
            "std_dev": variance ** 0.5,
            "min": min(data),
            "max": max(data)
        }
    
    def run(self):
        while True:
            cmd = input("\n🧮 Mathematicaclaw> ").strip()
            if not cmd:
                continue
            if cmd == '/quit':
                break
            if cmd == '/help':
                self._print_welcome()
                continue
            
            # /calc
            if cmd.startswith('/calc '):
                r = self.calc(cmd[6:])
                if r["success"]:
                    print(f"✅ {r['result']}")
                else:
                    print(f"❌ {r['error']}")
                continue
            
            # /solve
            if cmd.startswith('/solve '):
                r = self.solve(cmd[7:])
                if r["success"]:
                    print(f"✅ Solution: {r['result']}")
                else:
                    print(f"❌ {r['error']}")
                continue
            
            # /derive
            if cmd.startswith('/derive '):
                r = self.derive(cmd[8:])
                if r["success"]:
                    print(f"✅ {r['result']}")
                else:
                    print(f"❌ {r['error']}")
                continue
            
            # /integrate
            if cmd.startswith('/integrate '):
                expr = cmd[11:]
                if " from " in expr:
                    parts = expr.split(" from ")
                    expr2 = parts[0]
                    limits = parts[1].split(" to ")
                    a, b = float(limits[0]), float(limits[1])
                    r = self.integrate(expr2, a, b)
                else:
                    r = self.integrate(expr)
                if r["success"]:
                    print(f"✅ {r['result']}")
                else:
                    print(f"❌ {r['error']}")
                continue
            
            # /limit
            if cmd.startswith('/limit '):
                r = self.limit(cmd[7:])
                if r["success"]:
                    print(f"✅ Limit: {r['result']}")
                else:
                    print(f"❌ {r['error']}")
                continue
            
            # /taylor
            if cmd.startswith('/taylor '):
                r = self.taylor(cmd[8:])
                if r["success"]:
                    print(f"✅ {r['result']}")
                else:
                    print(f"❌ {r['error']}")
                continue
            
            # /plot
            if cmd.startswith('/plot '):
                r = self.plot(cmd[6:])
                if r["success"]:
                    print(f"✅ Plot saved to: {r['path']}")
                else:
                    print(f"❌ {r['error']}")
                continue
            
            # /stats
            if cmd.startswith('/stats '):
                try:
                    data = [float(x.strip()) for x in cmd[7:].split(',')]
                    r = self.stats(data)
                    if r["success"]:
                        print(f"✅ Count: {r['count']}, Mean: {r['mean']:.4f}, StdDev: {r['std_dev']:.4f}")
                    else:
                        print(f"❌ {r['error']}")
                except Exception as e:
                    print(f"❌ Error parsing data: {e}")
                continue
            
            print("Unknown command. Type /help")


def main():
    agent = Mathematicaclaw()
    agent.run()


if __name__ == "__main__":
    main()