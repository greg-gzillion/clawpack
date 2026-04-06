#!/usr/bin/env python3
\"\"\"Series module\"\"\"

import sympy as sp

class SeriesEngine:
    def taylor_series(self, expression, variable="x", point=0, order=5):
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            series = sp.series(expr, x, point, order).removeO()
            return {"success": True, "result": str(series)}
        except Exception as e:
            return {"success": False, "error": str(e)}