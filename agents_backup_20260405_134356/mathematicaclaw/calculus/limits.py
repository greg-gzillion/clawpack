"""Limits module for Mathematicaclaw"""

import sympy as sp
from typing import Dict, Any

class LimitEngine:
    """Handles limit calculations"""
    
    def __init__(self):
        self.sympy_available = True
    
    def calculate_limit(self, expression: str, variable: str = "x", 
                        point: float = 0, direction: str = "+") -> Dict[str, Any]:
        """Calculate limit of expression as variable approaches point"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            
            if direction == "+":
                result = sp.limit(expr, x, point, dir='+')
            elif direction == "-":
                result = sp.limit(expr, x, point, dir='-')
            else:
                result = sp.limit(expr, x, point)
            
            return {
                "success": True,
                "result": str(result),
                "expression": expression,
                "variable": variable,
                "point": point,
                "direction": direction
            }
        except Exception as e:
            return {"success": False, "error": str(e)}