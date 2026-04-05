"""Main Mathematicaclaw core class"""

import sympy as sp
from .shared.memory import SharedMemory
from .calculators.expression import ExpressionCalculator
from .calculators.calculus import CalculusEngine
from .calculators.plotting import PlottingEngine
from .calculators.statistics import StatisticsEngine

class MathematicaclawCore:
    def __init__(self):
        self.name = "Mathematicaclaw"
        self.shared = SharedMemory()
        self.expr_calc = ExpressionCalculator()
        self.calculus = CalculusEngine()
        self.plotting = PlottingEngine()
        self.stats_calc = StatisticsEngine()
        self.sympy_available = True
    
    def calculate(self, expression: str):
        return self.expr_calc.evaluate(expression)
    
    def solve(self, equation: str, variable: str = "x"):
        cached = self.shared.read(equation, "solve")
        if cached:
            return {"solution": cached, "source": "shared"}
        
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(equation.replace("=", "-"))
            solutions = sp.solve(expr, x)
            result = str(solutions)
            self.shared.write(equation, result, "solve", variable, self.name)
            return {"solution": result, "source": "sympy"}
        except Exception as e:
            return {"error": str(e)}
    
    def differentiate(self, expression: str, variable: str = "x", order: int = 1):
        cache_key = f"{expression}|{variable}|{order}"
        cached = self.shared.read(cache_key, "differentiate")
        if cached:
            return {"derivative": cached, "source": "shared"}
        
        result = self.calculus.differentiate(expression, variable, order)
        if result.get("success"):
            self.shared.write(cache_key, result["result"], "differentiate", f"{variable},{order}", self.name)
            return {"derivative": result["result"], "source": "sympy"}
        return {"error": result.get("error")}
    
    def integrate(self, expression: str, a: float = None, b: float = None):
        cache_key = f"{expression}|{a}|{b}"
        op_type = "integrate_definite" if a is not None else "integrate"
        cached = self.shared.read(cache_key, op_type)
        if cached:
            return {"result": cached, "type": "definite" if a is not None else "indefinite", "source": "shared"}
        
        result = self.calculus.integrate(expression, "x", a, b)
        if result.get("success"):
            self.shared.write(cache_key, result["result"], op_type, f"{a},{b}", self.name)
            return {"result": result["result"], "type": result.get("type"), "source": "sympy"}
        return {"error": result.get("error")}
    
    def limit(self, expression: str, point: float = 0):
        cache_key = f"{expression}|{point}"
        cached = self.shared.read(cache_key, "limit")
        if cached:
            return {"result": cached, "point": point, "source": "shared"}
        
        result = self.calculus.limit(expression, "x", point)
        if result.get("success"):
            self.shared.write(cache_key, result["result"], "limit", f"{point}", self.name)
            return {"result": result["result"], "point": point, "source": "sympy"}
        return {"error": result.get("error")}
    
    def taylor(self, expression: str, point: float = 0, order: int = 5):
        cache_key = f"{expression}|{point}|{order}"
        cached = self.shared.read(cache_key, "taylor")
        if cached:
            return {"result": cached, "point": point, "order": order, "source": "shared"}
        
        result = self.calculus.taylor(expression, "x", point, order)
        if result.get("success"):
            self.shared.write(cache_key, result["result"], "taylor", f"{point},{order}", self.name)
            return {"result": result["result"], "point": point, "order": order, "source": "sympy"}
        return {"error": result.get("error")}
    
    def plot(self, expression: str):
        return self.plotting.plot(expression)
    
    def statistics(self, data):
        return self.stats_calc.calculate(data)