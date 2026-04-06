#!/usr/bin/env python3
\"\"\"Plotting module for Mathematicaclaw\"\"\"

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from datetime import datetime
import os

class PlottingEngine:
    def __init__(self, plots_dir=None):
        if plots_dir is None:
            self.plots_dir = os.path.join(os.path.dirname(__file__), "..", "plots")
        else:
            self.plots_dir = plots_dir
        os.makedirs(self.plots_dir, exist_ok=True)
    
    def plot_function(self, expression, x_range=(-10, 10), title=None, save=True):
        try:
            x = sp.Symbol('x')
            expr = sp.sympify(expression)
            f = sp.lambdify(x, expr, modules=['numpy'])
            
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            y_vals = []
            for xv in x_vals:
                try:
                    yv = f(xv)
                    if isinstance(yv, complex) and abs(yv.imag) > 1e-10:
                        y_vals.append(np.nan)
                    else:
                        y_vals.append(float(yv.real))
                except:
                    y_vals.append(np.nan)
            
            y_vals = np.array(y_vals)
            
            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {expression}')
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            plt.grid(True, alpha=0.3)
            
            y_vals_finite = y_vals[np.isfinite(y_vals)]
            if len(y_vals_finite) > 0:
                y_min, y_max = np.min(y_vals_finite), np.max(y_vals_finite)
                margin = (y_max - y_min) * 0.1
                plt.ylim(y_min - margin, y_max + margin)
            
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.title(title or f'Plot of f(x) = {expression}')
            plt.legend()
            
            if save:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_expr = expression.replace('*', '_').replace('/', '_').replace('^', '_')
                filename = f"plot_{safe_expr[:30]}_{timestamp}.png"
                filepath = os.path.join(self.plots_dir, filename)
                plt.savefig(filepath, dpi=150, bbox_inches='tight')
                plt.close()
                return filepath
            else:
                plt.show()
                return None
        except Exception as e:
            return {"error": str(e)}
    
    def plot_multiple(self, expressions, x_range=(-10, 10), title=None, save=True):
        try:
            x = sp.Symbol('x')
            plt.figure(figsize=(10, 6))
            colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
            
            for i, expr_str in enumerate(expressions):
                expr = sp.sympify(expr_str)
                f = sp.lambdify(x, expr, modules=['numpy'])
                
                x_vals = np.linspace(x_range[0], x_range[1], 1000)
                y_vals = []
                for xv in x_vals:
                    try:
                        yv = f(xv)
                        if isinstance(yv, complex) and abs(yv.imag) > 1e-10:
                            y_vals.append(np.nan)
                        else:
                            y_vals.append(float(yv.real))
                    except:
                        y_vals.append(np.nan)
                
                color = colors[i % len(colors)]
                plt.plot(x_vals, y_vals, color=color, linewidth=2, label=f'f(x) = {expr_str}')
            
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            plt.grid(True, alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.title(title or 'Multiple Functions Plot')
            plt.legend()
            
            if save:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"plot_multiple_{timestamp}.png"
                filepath = os.path.join(self.plots_dir, filename)
                plt.savefig(filepath, dpi=150, bbox_inches='tight')
                plt.close()
                return filepath
            else:
                plt.show()
                return None
        except Exception as e:
            return {"error": str(e)}
    
    def list_plots(self):
        plots = []
        for f in os.listdir(self.plots_dir):
            if f.endswith('.png'):
                filepath = os.path.join(self.plots_dir, f)
                size = os.path.getsize(filepath) / 1024
                plots.append({"name": f, "size_kb": round(size, 1), "path": filepath})
        return plots
    
    def clear_plots(self):
        count = 0
        for f in os.listdir(self.plots_dir):
            if f.endswith('.png'):
                os.remove(os.path.join(self.plots_dir, f))
                count += 1
        return {"deleted": count}