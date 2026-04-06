#!/usr/bin/env python3
\"\"\"Limits module\"\"\"

import sympy as sp

class LimitEngine:
    def calculate_limit(self, expression, variable="x", point=0, direction="+"):
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            if direction == "+":
                result = sp.limit(expr, x, point, dir='+')
            else:
                result = sp.limit(expr, x, point)
            return {"success": True, "result": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}