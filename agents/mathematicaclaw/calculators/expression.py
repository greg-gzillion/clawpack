#!/usr/bin/env python3
\"\"\"Expression evaluation module\"\"\"

import sympy as sp

class ExpressionCalculator:
    def evaluate(self, expression):
        try:
            result = sp.sympify(expression)
            return {"result": str(result), "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}