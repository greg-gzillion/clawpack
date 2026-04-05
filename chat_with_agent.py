# chat_with_agent.py (UPDATED)
import sqlite3
import requests
import json
from pathlib import Path
import sys

class AgentChat:
    def __init__(self):
        self.db_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.ollama_url = "http://127.0.0.1:11434"
        
    def get_agent_knowledge(self, agent_name, query):
        """Retrieve relevant knowledge for the agent"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT tk.topic, tk.content 
            FROM agent_training at
            JOIN tx_knowledge tk ON at.topic = tk.topic
            WHERE at.agent = ? AND (tk.topic LIKE ? OR tk.content LIKE ?)
            LIMIT 3
        """, (agent_name, f"%{query}%", f"%{query}%"))
        
        knowledge = cursor.fetchall()
        conn.close()
        return knowledge
    
    def get_all_agent_knowledge(self, agent_name):
        """Get all knowledge for an agent"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT tk.topic, tk.content 
            FROM agent_training at
            JOIN tx_knowledge tk ON at.topic = tk.topic
            WHERE at.agent = ?
        """, (agent_name,))
        
        knowledge = cursor.fetchall()
        conn.close()
        return knowledge
    
    def chat(self, agent_name, user_message, model):
        """Chat with an agent using Ollama"""
        print(f"\n🤖 {agent_name.upper()} is thinking (using {model})...")
        
        knowledge = self.get_agent_knowledge(agent_name, user_message)
        
        roles = {
            "eagleclaw": "Main coding assistant and coordinator",
            "crustyclaw": "Bug detection and security specialist",
            "rustypycraw": "Code generation and optimization expert",
            "claw-coder": "Python AI and machine learning assistant",
            "claw-code": "Claude reimplementation and general AI",
            "agentforlaw": "Legal contracts and compliance specialist",
            "sysclaw": "System maintenance and operations"
        }
        
        context = f"You are {agent_name}, {roles.get(agent_name, 'AI Assistant')} in the Clawpack ecosystem.\n\n"
        
        if knowledge:
            context += "RELEVANT KNOWLEDGE FROM TX BLOCKCHAIN:\n"
            for topic, content in knowledge:
                context += f"\n[{topic}]\n{content[:500]}\n"
            context += "\n"
        
        context += f"USER QUESTION: {user_message}\n\n"
        context += "Please provide a helpful, accurate response based on your knowledge."
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": context,
                    "stream": False,
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

def main():
    chat = AgentChat()
    
    print("🦞 Clawpack Agent Chat System - Enhanced Edition")
    print("=" * 55)
    print("\nAvailable Agents:")
    agents = ["eagleclaw", "crustyclaw", "rustypycraw", "claw-coder", "agentforlaw", "sysclaw"]
    for i, agent in enumerate(agents, 1):
        print(f"  {i}. {agent}")
    
    print("\n🌟 Available Models (NEW!):")
    print("  1. gemma3:27b     🏆 BEST QUALITY - 17GB (Ultra)")
    print("  2. qwen3-coder:30b 💻 EXPERT CODING - 18GB")
    print("  3. deepseek-r1:8b  🧠 REASONING - 5GB")
    print("  4. gemma3:12b     ⚖️ BALANCED - 8.1GB")
    print("  5. deepseek-coder:6.7b 💻 CODING - 3.8GB")
    print("  6. llama3.2:3b    📝 GENERAL - 2GB")
    print("  7. gemma3:1b      🚀 FASTEST - 815MB")
    print("  8. gemma3:4b      ⚡ MEDIUM - 3.3GB (downloading)")
    
    print("\n💡 Tip: Use gemma3:27b for complex questions, qwen3-coder for coding")
    print("\nType 'quit' to exit\n")
    
    while True:
        print("-" * 55)
        agent_choice = input("Select agent (number or name, or 'quit'): ").strip().lower()
        
        if agent_choice == 'quit':
            break
        
        if agent_choice.isdigit():
            idx = int(agent_choice) - 1
            if 0 <= idx < len(agents):
                agent_name = agents[idx]
            else:
                print(f"Invalid agent number. Choose 1-{len(agents)}")
                continue
        elif agent_choice in agents:
            agent_name = agent_choice
        else:
            print(f"Unknown agent. Choose from: {', '.join(agents)}")
            continue
        
        model_choice = input("Choose model (1-8, default 1 for gemma3:27b): ").strip()
        model_map = {
            "1": "gemma3:27b",
            "2": "qwen3-coder:30b",
            "3": "deepseek-r1:8b",
            "4": "gemma3:12b",
            "5": "deepseek-coder:6.7b",
            "6": "llama3.2:3b",
            "7": "gemma3:1b",
            "8": "gemma3:4b"
        }
        model = model_map.get(model_choice, "gemma3:27b")
        
        question = input("Your question: ").strip()
        if question.lower() == 'quit':
            break
        
        if not question:
            print("Please enter a question.")
            continue
        
        response = chat.chat(agent_name, question, model)
        print(f"\n💬 {agent_name.upper()} responds:\n")
        print(response)
        print()

if __name__ == "__main__":
    main()
