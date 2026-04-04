
class Harness:
    """The harness is the product - not the model"""
    def __init__(self):
        self.tools = ['search', 'read', 'grep', 'pinch', 'audit']
        self.rules = self._load_rules()
        self.memory = self._load_memory()
    
    def execute(self, task: str) -> str:
        # Apply rules first
        # Then use tools
        # Finally query model if needed
        pass
