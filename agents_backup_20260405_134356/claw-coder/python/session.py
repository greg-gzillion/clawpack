
class PersistentSession:
    """Memory that persists across CLI sessions"""
    def __init__(self):
        self.memory_file = os.path.expanduser("~/.rustypycraw/memory.json")
        self.conversations = self._load()
    
    def remember(self, key: str, value: str):
        """Store information across sessions"""
        self.conversations[key] = value
        self._save()
    
    def recall(self, key: str) -> str:
        """Retrieve cross-session memory"""
        return self.conversations.get(key, "")
