#!/usr/bin/env python3
\"\"\"Integration module\"\"\"

import sympy as sp

class IntegrationEngine:
    def integrate(self, expression, variable="x", a=None, b=None):
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            if a is not None and b is not None:
                result = sp.integrate(expr, (x, a, b))
                return {"success": True, "result": str(result), "type": "definite"}
            else:
                result = sp.integrate(expr, x)
                return {"success": True, "result": str(result) + " + C", "type": "indefinite"}
        except Exception as e:
            return {"success": False, "error": str(e)}