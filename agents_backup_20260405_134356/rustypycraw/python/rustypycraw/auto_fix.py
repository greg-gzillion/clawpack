"""
Automatic code fixing for common Rust/CosmWasm issues
"""

import re
import subprocess

class AutoFix:
    """Automatically fix common code issues"""
    
    @classmethod
    def fix_unnecessary_clones(cls, filepath: str) -> int:
        """Replace unnecessary .clone() with references"""
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Pattern: .clone() on references
        pattern = r'(\w+)\.clone\(\)'
        fixed = re.sub(pattern, r'&(\1)', content)
        
        # Count changes
        changes = content.count('.clone()') - fixed.count('.clone()')
        
        if changes > 0:
            with open(filepath, 'w') as f:
                f.write(fixed)
        
        return changes
    
    @classmethod
    def add_error_handling(cls, filepath: str) -> int:
        """Add proper error handling to functions"""
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Find functions without error handling
        pattern = r'fn (\w+)\([^)]*\) -> [^{]+{([^}]+)}'
        matches = re.findall(pattern, content, re.DOTALL)
        
        changes = 0
        for func_name, body in matches:
            if 'Result' in body and '?' not in body:
                # Add ? operator to Result returns
                new_body = re.sub(r'(\w+)\([^)]+\)', r'\1()?', body)
                content = content.replace(body, new_body)
                changes += 1
        
        if changes > 0:
            with open(filepath, 'w') as f:
                f.write(content)
        
        return changes
    
    @classmethod
    fn run_clippy(cls, project_path: str) -> list:
        """Run clippy and return suggestions"""
        result = subprocess.run(
            f"cd {project_path} && cargo clippy -- -D warnings 2>&1",
            shell=True, capture_output=True, text=True
        )
        
        suggestions = []
        for line in result.stdout.split('\n'):
            if 'warning' in line or 'error' in line:
                suggestions.append(line)
        
        return suggestions
