#!/usr/bin/env python3
\"\"\"Derivative module\"\"\"

import sympy as sp

class DerivativeEngine:
    def differentiate(self, expression, variable="x", order=1):
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            deriv = sp.diff(expr, x, order)
            return {"success": True, "result": str(deriv)}
        except Exception as e:
            return {"success": False, "error": str(e)}