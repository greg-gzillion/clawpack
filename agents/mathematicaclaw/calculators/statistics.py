"""Statistics module"""

from typing import Dict, List, Any

class StatisticsEngine:
    def calculate(self, data: List[float]) -> Dict[str, Any]:
        if not data:
            return {"error": "No data provided"}
        
        n = len(data)
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        sorted_data = sorted(data)
        
        return {
            "count": n,
            "sum": sum(data),
            "mean": mean,
            "median": sorted_data[n // 2] if n % 2 else (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2,
            "variance": variance,
            "std_dev": variance ** 0.5,
            "min": min(data),
            "max": max(data),
            "range": max(data) - min(data)
        }