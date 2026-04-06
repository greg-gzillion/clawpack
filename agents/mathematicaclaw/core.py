#!/usr/bin/env python3
\"\"\"Mathematicaclaw - Core Engine\"\"\"

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculators.expression import ExpressionCalculator
from calculators.statistics import StatisticsCalculator
from calculators.plotting import PlottingEngine
from calculus.derivative import DerivativeEngine
from calculus.integration import IntegrationEngine
from calculus.limits import LimitEngine
from calculus.series import SeriesEngine

import sympy as sp
import sqlite3
from datetime import datetime

class SharedMemory:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.db_path = Path.home() / ".claw_memory" / "mathematicaclaw.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS calculations (key TEXT PRIMARY KEY, result TEXT, op_type TEXT, params TEXT, agent TEXT, timestamp TEXT)")
        conn.commit()
        conn.close()
    
    def read(self, key, op_type):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT result FROM calculations WHERE key = ? AND op_type = ?", (key, op_type))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    
    def write(self, key, result, op_type, params, agent):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO calculations VALUES (?,?,?,?,?,?)", (key, str(result), op_type, params, agent, datetime.now().isoformat()))
        conn.commit()
        conn.close()

class MathematicaclawCore:
    def __init__(self):
        self.name = "mathematicaclaw"
        self.shared = SharedMemory(self.name)
        self.expr_calc = ExpressionCalculator()
        self.stats_calc = StatisticsCalculator()
        self.plotting_engine = PlottingEngine()
        self.derivative_engine = DerivativeEngine()
        self.integration_engine = IntegrationEngine()
        self.limit_engine = LimitEngine()
        self.series_engine = SeriesEngine()
        self.plots_dir = self.plotting_engine.plots_dir
    
    def calculate(self, expression):
        try:
            expr = expression.replace("^", "**")
            result = self.expr_calc.evaluate(expr)
            return result
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def solve(self, equation, variable="x"):
        try:
            x = sp.Symbol(variable)
            if "=" in equation:
                left, right = equation.split("=")
                expr = sp.sympify(left) - sp.sympify(right)
            else:
                expr = sp.sympify(equation)
            solutions = sp.solve(expr, x)
            return {"solution": str(solutions), "source": "sympy"}
        except Exception as e:
            return {"error": str(e)}
    
    def derivative(self, expression, variable="x", order=1):
        result = self.derivative_engine.differentiate(expression, variable, order)
        if result.get("success"):
            return {"derivative": result.get("result"), "source": "sympy"}
        return {"error": result.get("error", "Unknown error")}
    
    def integrate(self, expression, a=None, b=None):
        result = self.integration_engine.integrate(expression, "x", a, b)
        if result.get("success"):
            return {"result": result.get("result"), "type": result.get("type"), "source": "sympy"}
        return {"error": result.get("error", "Unknown error")}
    
    def limit(self, expression, point=0, direction="+"):
        result = self.limit_engine.calculate_limit(expression, "x", point, direction)
        if result.get("success"):
            return {"result": result.get("result"), "point": point, "source": "sympy"}
        return {"error": result.get("error", "Unknown error")}
    
    def statistics(self, numbers):
        return self.stats_calc.calculate(numbers)
    
    def plot_function(self, expression, x_range=(-10, 10)):
        return self.plotting_engine.plot_function(expression, x_range)
    
    def plot_multiple(self, expressions):
        return self.plotting_engine.plot_multiple(expressions)
    
    def list_plots(self):
        return self.plotting_engine.list_plots()
    
    def clear_plots(self):
        return self.plotting_engine.clear_plots()