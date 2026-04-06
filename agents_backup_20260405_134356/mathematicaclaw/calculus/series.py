"""Series expansion module for Mathematicaclaw"""

import sympy as sp
from typing import Dict, Any

class SeriesEngine:
    """Handles Taylor, Laurent, and Fourier series"""
    
    def __init__(self):
        self.sympy_available = True
    
    def taylor_series(self, expression: str, variable: str = "x", 
                      point: float = 0, order: int = 5) -> Dict[str, Any]:
        """Calculate Taylor series expansion"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            series = sp.series(expr, x, point, order)
            
            return {
                "success": True,
                "result": str(series),
                "expression": expression,
                "point": point,
                "order": order
            }
        except Exception as e:
            return {"success": False, "error": str(e)}