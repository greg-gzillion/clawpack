import os
# polyclaw.py - Polyclaw: Multi-Language Translation Agent (Enhanced)
import requests

# Your working API key
CLOUD_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

class Polyclaw:
    def __init__(self):
        self.name = "Polyclaw"
        self.role = "I translate between 35+ languages"
        
        # Complete language list - 35+ languages
        self.languages = {
            # Major languages
            "en": "English",
            "es": "Spanish",
            "fr": "French", 
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh": "Chinese (Simplified)",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            
            # Added languages
            "bn": "Bengali",
            "pa": "Punjabi",
            "ur": "Urdu",
            "te": "Telugu",
            "ta": "Tamil",
            "mr": "Marathi",
            "gu": "Gujarati",
            "kn": "Kannada",
            "ml": "Malayalam",
            
            "tr": "Turkish",
            "nl": "Dutch",
            "pl": "Polish",
            "sv": "Swedish",
            "da": "Danish",
            "no": "Norwegian",
            "fi": "Finnish",
            "el": "Greek",
            "cs": "Czech",
            "hu": "Hungarian",
            "ro": "Romanian",
            "vi": "Vietnamese",
            "th": "Thai",
            "id": "Indonesian",
            "ms": "Malay",
            "tl": "Filipino/Tagalog",
            "he": "Hebrew",
            "iw": "Hebrew (alt)",
            "uk": "Ukrainian",
            "bg": "Bulgarian",
            "sr": "Serbian",
            "hr": "Croatian",
            "sk": "Slovak",
            "sl": "Slovenian",
            "lt": "Lithuanian",
            "lv": "Latvian",
            "et": "Estonian",
            "is": "Icelandic",
            "mt": "Maltese",
            "af": "Afrikaans",
            "sw": "Swahili",
            "am": "Amharic",
            "ne": "Nepali",
            "si": "Sinhala",
            "my": "Burmese",
            "km": "Khmer",
            "lo": "Lao",
            "mn": "Mongolian"
        }
        
        # Group languages by region for display
        self.regions = {
            "ðŸŒŽ Major Languages": ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko", "ar", "hi"],
            "ðŸ‡®ðŸ‡³ Indian Subcontinent": ["bn", "pa", "ur", "te", "ta", "mr", "gu", "kn", "ml", "ne", "si"],
            "ðŸ‡ªðŸ‡º European": ["nl", "pl", "sv", "da", "no", "fi", "el", "cs", "hu", "ro", "uk", "bg", "sr", "hr", "sk", "sl", "lt", "lv", "et", "is", "mt"],
            "ðŸŒ Southeast Asian": ["vi", "th", "id", "ms", "tl", "my", "km", "lo"],
            "ðŸŒ African/Middle Eastern": ["he", "iw", "ar", "am", "sw", "af"],
            "ðŸŒ Other Asian": ["mn"]
        }
    
    def translate(self, text, to_lang, from_lang="auto"):
        """Translate text to target language"""
        
        if to_lang not in self.languages:
            return f"Language '{to_lang}' not supported. Use /list to see all languages."
        
        to_name = self.languages.get(to_lang, to_lang)
        from_text = f" from {self.languages.get(from_lang, 'auto')}" if from_lang != "auto" else ""
        
        prompt = f"""Translate the following text{from_text} to {to_name}. 
Only output the translation, nothing else. Keep the same tone and meaning.

TEXT: {text}

TRANSLATION:"""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def show_languages(self):
        """Display all languages by region"""
        print("\n" + "="*70)
        print("ðŸŒ AVAILABLE LANGUAGES (35+ languages)")
        print("="*70)
        
        for region, langs in self.regions.items():
            print(f"\n{region}:")
            line = ""
            for code in langs:
                name = self.languages.get(code, code)
                line += f"  {code} - {name}"
                # Group in columns
                if len(line) > 60:
                    print(line)
                    line = ""
            if line:
                print(line)
        
        print("\n" + "="*70)
        print("ðŸ’¡ Tip: Use language codes like 'en', 'es', 'fr', 'de', 'zh', 'ja', 'ar', 'hi', etc.")
        print("="*70)
    
    def chat(self):
        print("\n" + "="*70)
        print("ðŸ¦ž POLYCLAW ENHANCED - 35+ Language Translation Agent")
        print("="*70)
        
        self.show_languages()
        
        print("\nCommands:")
        print("  /to [lang] [text]  - Translate to language")
        print("  /list              - Show all languages again")
        print("  /help              - This menu")
        print("  /quit              - Exit")
        print("\nExamples:")
        print("  /to es Hello, how are you?")
        print("  /to fr What is TX blockchain?")
        print("  /to bn Smart Tokens are programmable")
        print("  /to ta Explain compliance features")
        print("="*70)
        
        while True:
            cmd = input("\nðŸŒ Polyclaw> ").strip()
            
            if not cmd:
                continue
            if cmd == '/quit':
                break
            if cmd == '/help':
                print("\nCommands: /to [lang] [text], /list, /help, /quit")
                continue
            if cmd == '/list':
                self.show_languages()
                continue
            
            if cmd.startswith('/to '):
                parts = cmd[4:].split(' ', 1)
                if len(parts) < 2:
                    print("Usage: /to [language] [text]")
                    print("Example: /to es Hello world")
                    continue
                
                target_lang = parts[0].lower()
                text = parts[1]
                
                if target_lang not in self.languages:
                    print(f"Unknown language: {target_lang}")
                    print(f"Type /list to see all 35+ supported languages")
                    continue
                
                print(f"\nðŸ¦ž Translating to {self.languages[target_lang]}...\n")
                result = self.translate(text, target_lang)
                print(f"\nðŸ“ TRANSLATION ({self.languages[target_lang]}):\n{result}\n")
                print("-"*50)
            else:
                print("Unknown command. Use /to [lang] [text] or /help")

def main():
    poly = Polyclaw()
    poly.chat()

if __name__ == "__main__":
    main()
