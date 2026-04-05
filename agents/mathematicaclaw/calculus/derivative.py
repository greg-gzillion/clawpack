"""Derivative calculus module for Mathematicaclaw"""

import sympy as sp
from typing import Dict, Any, Optional, Union

class DerivativeEngine:
    """Handles symbolic and numerical differentiation"""
    
    def __init__(self):
        self.sympy_available = True  # We know SymPy is installed
    
    def differentiate(self, expression: str, variable: str = "x", order: int = 1) -> Dict[str, Any]:
        """Calculate derivative of expression"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            deriv = sp.diff(expr, x, order)
            
            # Simplify result
            deriv_simplified = sp.simplify(deriv)
            
            return {
                "success": True,
                "result": str(deriv_simplified),
                "original": expression,
                "variable": variable,
                "order": order
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def partial_derivative(self, expression: str, variables: list) -> Dict[str, Any]:
        """Calculate partial derivatives"""
        try:
            symbols = [sp.Symbol(v) for v in variables]
            expr = sp.sympify(expression)
            
            results = {}
            for var in symbols:
                deriv = sp.diff(expr, var)
                results[str(var)] = str(sp.simplify(deriv))
            
            return {"success": True, "partials": results}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def gradient(self, expression: str, variables: list) -> Dict[str, Any]:
        """Calculate gradient vector"""
        try:
            symbols = [sp.Symbol(v) for v in variables]
            expr = sp.sympify(expression)
            
            gradient = []
            for var in symbols:
                deriv = sp.diff(expr, var)
                gradient.append(str(sp.simplify(deriv)))
            
            return {"success": True, "gradient": gradient, "variables": variables}
        except Exception as e:
            return {"success": False, "error": str(e)}