
RULES_DIR = ".rustypycraw/rules"

def load_project_rules(project_path: str) -> str:
    """Load project-specific rules from .rustypycraw/rules/"""
    rules_path = os.path.join(project_path, RULES_DIR)
    if os.path.exists(rules_path):
        rules = []
        for f in os.listdir(rules_path):
            if f.endswith('.md'):
                with open(os.path.join(rules_path, f), 'r') as file:
                    rules.append(f"## {f}\n{file.read()}")
        return "\n\n".join(rules)
    return ""
