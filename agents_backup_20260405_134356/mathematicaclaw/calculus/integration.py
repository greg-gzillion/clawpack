"""Integration module for Mathematicaclaw"""

import sympy as sp
from typing import Dict, Any, Optional

class IntegrationEngine:
    """Handles symbolic and numerical integration"""
    
    def __init__(self):
        self.sympy_available = True
    
    def integrate(self, expression: str, variable: str = "x", 
                  a: Optional[float] = None, b: Optional[float] = None) -> Dict[str, Any]:
        """Calculate integral (indefinite or definite)"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            
            if a is not None and b is not None:
                # Definite integral
                result = sp.integrate(expr, (x, a, b))
                result_type = "definite"
            else:
                # Indefinite integral
                result = sp.integrate(expr, x)
                result_type = "indefinite"
            
            return {
                "success": True,
                "result": str(result),
                "type": result_type,
                "expression": expression,
                "variable": variable
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def double_integral(self, expression: str, var1: str = "x", var2: str = "y",
                        limits1: tuple = None, limits2: tuple = None) -> Dict[str, Any]:
        """Calculate double integral"""
        try:
            x = sp.Symbol(var1)
            y = sp.Symbol(var2)
            expr = sp.sympify(expression)
            
            if limits1 and limits2:
                result = sp.integrate(expr, (x, limits1[0], limits1[1]), 
                                            (y, limits2[0], limits2[1]))
            else:
                result = sp.integrate(expr, x, y)
            
            return {"success": True, "result": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}