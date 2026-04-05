"""Calculus operations: derivatives, integrals, limits, series"""

import sympy as sp
from typing import Dict, Any, Optional

class CalculusEngine:
    def __init__(self):
        self.sympy_available = True
    
    def differentiate(self, expression: str, variable: str = "x", order: int = 1) -> Dict[str, Any]:
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            deriv = sp.diff(expr, x, order)
            return {"success": True, "result": str(sp.simplify(deriv))}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def integrate(self, expression: str, variable: str = "x", a: float = None, b: float = None) -> Dict[str, Any]:
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            if a is not None and b is not None:
                result = sp.integrate(expr, (x, a, b))
                result_str = f"{result:.6f}" if isinstance(result, (int, float)) else str(result)
                return {"success": True, "result": result_str, "type": "definite"}
            else:
                result = sp.integrate(expr, x)
                return {"success": True, "result": str(result), "type": "indefinite"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def limit(self, expression: str, variable: str = "x", point: float = 0) -> Dict[str, Any]:
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            result = sp.limit(expr, x, point)
            return {"success": True, "result": str(result), "point": point}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def taylor(self, expression: str, variable: str = "x", point: float = 0, order: int = 5) -> Dict[str, Any]:
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            series = sp.series(expr, x, point, order)
            return {"success": True, "result": str(series), "point": point, "order": order}
        except Exception as e:
            return {"success": False, "error": str(e)}