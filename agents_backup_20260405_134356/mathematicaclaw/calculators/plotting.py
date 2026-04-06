"""Function plotting module"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class PlottingEngine:
    def __init__(self):
        self.plot_path = Path.home() / ".claw_memory" / "plots"
        self.plot_path.mkdir(parents=True, exist_ok=True)
    
    def plot(self, expression: str, var_min: float = -10, var_max: float = 10) -> Dict[str, Any]:
        try:
            expr_fixed = expression.replace('^', '**')
            x_vals = np.linspace(var_min, var_max, 1000)
            
            def f(x):
                local_dict = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan,
                              "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "e": np.e}
                return eval(expr_fixed, {"__builtins__": {}}, local_dict)
            
            y_vals = [f(x) for x in x_vals]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_vals, y_vals, 'b-', linewidth=2)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            ax.grid(True, alpha=0.3)
            ax.set_title(f'Plot of {expression}')
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            plot_file = self.plot_path / f"plot_{timestamp}.png"
            plt.savefig(plot_file, dpi=150, bbox_inches='tight')
            plt.close()
            
            return {"success": True, "path": str(plot_file), "expression": expression}
        except Exception as e:
            return {"success": False, "error": str(e)}