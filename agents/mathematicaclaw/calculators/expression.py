"""Expression evaluation module"""

import math
import cmath
from typing import Dict, Any

class ExpressionCalculator:
    def evaluate(self, expression: str) -> Dict[str, Any]:
        result = {"expression": expression, "value": None, "error": None, "type": None}
        expr = expression.strip()
        
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names.update({"i": 1j, "j": 1j, "pi": math.pi, "e": math.e})
        allowed_names.update({k: v for k, v in cmath.__dict__.items() if not k.startswith("__")})
        
        try:
            code = compile(expr, "<string>", "eval")
            for name in code.co_names:
                if name not in allowed_names and name not in ["abs", "round", "min", "max", "pow", "int", "float", "complex"]:
                    raise NameError(f"Function '{name}' not allowed")
            
            result["value"] = eval(code, {"__builtins__": {}}, allowed_names)
            result["type"] = type(result["value"]).__name__
            
            if isinstance(result["value"], complex):
                result["value_str"] = f"{result['value'].real:.10g}{result['value'].imag:+.10g}j"
            else:
                result["value_str"] = str(result["value"])
        except Exception as e:
            result["error"] = str(e)
        
        return result