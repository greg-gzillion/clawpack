#!/usr/bin/env python3
\"\"\"Statistics module\"\"\"

class StatisticsCalculator:
    def calculate(self, numbers):
        try:
            nums = [float(n.strip()) for n in numbers.split(",")]
            mean = sum(nums) / len(nums)
            return {"count": len(nums), "sum": sum(nums), "mean": mean, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}