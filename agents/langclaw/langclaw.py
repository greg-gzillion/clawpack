#!/usr/bin/env python3
"""
LangClaw - Language Tutor with Sound & Real Translations!
"""

import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime

# Add paths
CLAW_SHARED = Path(__file__).parent.parent / "claw_shared"
POLYCLAW_PATH = Path(__file__).parent.parent / "polyclaw"

sys.path.insert(0, str(CLAW_SHARED))
sys.path.insert(0, str(POLYCLAW_PATH))

# Import Polyclaw
POLYCLAW_AVAILABLE = False
polyclaw = None
try:
    from polyclaw_shared import PolyclawShared
    polyclaw = PolyclawShared()
    POLYCLAW_AVAILABLE = True
    print("? Polyclaw connected")
except Exception as e:
    print(f"?? Polyclaw not available: {e}")

# Import TTS
TTS_AVAILABLE = False
try:
    import pyttsx3
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)
    TTS_AVAILABLE = True
    print("? Text-to-speech ready")
except Exception as e:
    print(f"?? TTS not available: {e}")

class LangClaw:
    def __init__(self):
        self.db_path = Path.home() / ".claw_memory" / "langclaw_progress.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_db()
        
        # Language mappings
        self.languages = {
            "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
            "pt": "Portuguese", "ru": "Russian", "zh": "Chinese", "ja": "Japanese",
            "ko": "Korean", "ar": "Arabic", "hi": "Hindi", "tr": "Turkish",
            "nl": "Dutch", "pl": "Polish", "sv": "Swedish", "vi": "Vietnamese",
            "th": "Thai", "id": "Indonesian", "ms": "Malay", "he": "Hebrew",
            "el": "Greek", "cs": "Czech", "hu": "Hungarian", "ro": "Romanian",
            "uk": "Ukrainian", "da": "Danish", "fi": "Finnish", "no": "Norwegian",
            "hr": "Croatian", "sk": "Slovak", "sl": "Slovenian", "lt": "Lithuanian",
            "lv": "Latvian", "et": "Estonian", "bg": "Bulgarian"
        }
        
        # Common word translations for fallback
        self.common_words = {
            ("es", "hello"): "hola", ("es", "good morning"): "buenos d?as",
            ("es", "thank you"): "gracias", ("es", "goodbye"): "adi?s",
            ("fr", "hello"): "bonjour", ("fr", "good morning"): "bonjour",
            ("fr", "thank you"): "merci", ("fr", "goodbye"): "au revoir",
            ("de", "hello"): "hallo", ("de", "good morning"): "guten morgen",
            ("de", "thank you"): "danke", ("de", "goodbye"): "auf wiedersehen",
            ("it", "hello"): "ciao", ("it", "thank you"): "grazie",
            ("it", "goodbye"): "arrivederci", ("ja", "hello"): "?????",
            ("ja", "thank you"): "?????", ("ja", "good morning"): "?????????",
            ("zh", "hello"): "??", ("zh", "thank you"): "??",
            ("ko", "hello"): "?????", ("ko", "thank you"): "?????"
        }
        
        print("="*60)
        print("?? LangClaw - Language Tutor with Sound!")
        print("="*60)
        print(f"?? Languages: {len(self.languages)}")
        print(f"?? Sound: {'ON' if TTS_AVAILABLE else 'OFF'}")
        print(f"?? Polyclaw: {'Connected' if POLYCLAW_AVAILABLE else 'No'}")
        print("="*60)
    
    def init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS vocabulary
                     (lang TEXT, word TEXT, translation TEXT, mastery INTEGER DEFAULT 1,
                      learned_date TEXT, UNIQUE(lang, word))''')
        c.execute('''CREATE TABLE IF NOT EXISTS progress
                     (lang TEXT PRIMARY KEY, words_learned INTEGER DEFAULT 0,
                      quizzes_taken INTEGER DEFAULT 0, quiz_score REAL DEFAULT 0)''')
        conn.commit()
        conn.close()
    
    def speak(self, text):
        if TTS_AVAILABLE:
            try:
                tts_engine.say(text)
                tts_engine.runAndWait()
            except:
                pass
    
    def translate(self, text, target):
        """Get real translation"""
        text_lower = text.lower().strip()
        
        # Check common words dictionary first
        key = (target, text_lower)
        if key in self.common_words:
            return self.common_words[key]
        
        # Try Polyclaw
        if POLYCLAW_AVAILABLE and polyclaw:
            try:
                # Use the /to command format that Polyclaw understands
                result = polyclaw.translate(text, target)
                if result and result != text:
                    return result
            except:
                pass
        
        # Fallback - try to get from database if already learned
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT translation FROM vocabulary WHERE lang = ? AND word = ?", (target, text_lower))
        row = c.fetchone()
        conn.close()
        if row:
            return row[0]
        
        return f"?{text}?"  # Indicates translation not found
    
    def learn_word(self, lang, word):
        translation = self.translate(word, lang)
        
        # Don't save if translation failed
        if translation.startswith("?"):
            return f"\n?? Could not translate '{word}' to {self.languages.get(lang, lang)}. Try another word.\n"
        
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        try:
            c.execute("INSERT INTO vocabulary (lang, word, translation, learned_date) VALUES (?,?,?,?)",
                      (lang, word.lower(), translation, datetime.now().isoformat()))
            c.execute("INSERT OR IGNORE INTO progress (lang, words_learned) VALUES (?,0)", (lang,))
            c.execute("UPDATE progress SET words_learned = words_learned + 1 WHERE lang = ?", (lang,))
            conn.commit()
            
            # Speak!
            print(f"\n?? '{word}' ? '{translation}'")
            self.speak(word)
            self.speak(translation)
            
            return f"\n? Learned: {word} ? {translation}\n?? Language: {self.languages.get(lang, lang)}\n"
        except sqlite3.IntegrityError:
            return f"\n?? '{word}' already in your vocabulary!\n"
        finally:
            conn.close()
    
    def show_progress(self, lang):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT words_learned, quizzes_taken, quiz_score FROM progress WHERE lang = ?", (lang,))
        row = c.fetchone()
        c.execute("SELECT COUNT(*) FROM vocabulary WHERE lang = ?", (lang,))
        word_count = c.fetchone()[0]
        conn.close()
        
        if row and row[0] is not None:
            words, quizzes, score = row
        else:
            words, quizzes, score = 0, 0, 0.0
        
        # Handle None values
        quizzes = quizzes or 0
        score = score or 0.0
        
        return f"""
?? PROGRESS: {self.languages.get(lang, lang)}
???????????????????????????????????
  ?? Words learned: {word_count}
  ?? Quizzes taken: {quizzes}
  ? Average score: {score:.1f}%
"""
    
    def take_quiz(self, lang):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT word, translation FROM vocabulary WHERE lang = ? ORDER BY RANDOM() LIMIT 5", (lang,))
        words = c.fetchall()
        conn.close()
        
        if not words:
            return "?? No words learned yet! Use /learn first."
        
        print(f"\n{'='*50}")
        print(f"?? QUIZ - {self.languages.get(lang, lang)}")
        print(f"{'='*50}")
        
        score = 0
        for i, (word, translation) in enumerate(words, 1):
            print(f"\n{i}. What is '{word}'?")
            self.speak(word)
            input("   Press Enter for answer...")
            print(f"   ? Answer: {translation}")
            score += 1
        
        percentage = (score / len(words)) * 100
        
        # Update progress
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        current = c.execute("SELECT quizzes_taken, quiz_score FROM progress WHERE lang = ?", (lang,)).fetchone()
        if current:
            new_quizzes = (current[0] or 0) + 1
            old_score = current[1] or 0
            old_quizzes = current[0] or 0
            if old_quizzes > 0:
                new_score = ((old_score * old_quizzes) + percentage) / new_quizzes
            else:
                new_score = percentage
            c.execute("UPDATE progress SET quizzes_taken = ?, quiz_score = ? WHERE lang = ?",
                      (new_quizzes, new_score, lang))
        else:
            c.execute("INSERT INTO progress (lang, quizzes_taken, quiz_score) VALUES (?,?,?)",
                      (lang, 1, percentage))
        conn.commit()
        conn.close()
        
        print(f"\n{'='*50}")
        print(f"?? Score: {score}/{len(words)} ({percentage:.0f}%)")
        if percentage >= 80:
            print(f"   ?? Excellent!")
        elif percentage >= 60:
            print(f"   ?? Good job!")
        else:
            print(f"   ?? Keep practicing!")
        print(f"{'='*50}")
        return ""
    
    def practice(self, lang, word):
        translation = self.translate(word, lang)
        print(f"\n??? PRONUNCIATION: {word}")
        print(f"   Translation: {translation}")
        print("   Listening...")
        self.speak(word)
        self.speak(translation)
        print("   ?? Now you try!\n")
        return ""
    
    def chat(self):
        print("\n?? COMMANDS:")
        print("  /languages              - List all languages")
        print("  /learn [lang] [word]    - Learn a word (with sound!)")
        print("  /progress [lang]        - Show your progress")
        print("  /quiz [lang]            - Take a quiz")
        print("  /vocab [lang]           - List your vocabulary")
        print("  /practice [lang] [word] - Practice pronunciation")
        print("  /translate [lang] [text]- Translate text")
        print("  /speak [text]           - Speak any text")
        print("  /quit                   - Exit\n")
        
        while True:
            try:
                cmd = input("?? LangClaw> ").strip().lower()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("?? Goodbye! Keep practicing!")
                    break
                
                elif cmd == "/languages":
                    print("\n?? Languages:")
                    for code, name in sorted(self.languages.items()):
                        print(f"  {code}: {name}")
                    print(f"\n  Total: {len(self.languages)}")
                
                elif cmd.startswith("/learn "):
                    parts = cmd.split(maxsplit=2)
                    if len(parts) >= 3:
                        print(self.learn_word(parts[1], parts[2]))
                    else:
                        print("Usage: /learn [lang] [word]")
                        print("Example: /learn es gracias")
                
                elif cmd.startswith("/progress "):
                    parts = cmd.split()
                    if len(parts) >= 2:
                        print(self.show_progress(parts[1]))
                    else:
                        print("Usage: /progress [lang]")
                
                elif cmd.startswith("/quiz "):
                    parts = cmd.split()
                    if len(parts) >= 2:
                        self.take_quiz(parts[1])
                    else:
                        print("Usage: /quiz [lang]")
                
                elif cmd.startswith("/vocab "):
                    parts = cmd.split()
                    if len(parts) >= 2:
                        conn = sqlite3.connect(str(self.db_path))
                        c = conn.cursor()
                        c.execute("SELECT word, translation FROM vocabulary WHERE lang = ?", (parts[1],))
                        words = c.fetchall()
                        conn.close()
                        if words:
                            print(f"\n?? Your vocabulary ({len(words)} words):")
                            for w, t in words:
                                print(f"  {w} ? {t}")
                        else:
                            print("No words yet. Use /learn!")
                    else:
                        print("Usage: /vocab [lang]")
                
                elif cmd.startswith("/practice "):
                    parts = cmd.split(maxsplit=2)
                    if len(parts) >= 3:
                        self.practice(parts[1], parts[2])
                    else:
                        print("Usage: /practice [lang] [word]")
                
                elif cmd.startswith("/translate "):
                    parts = cmd.split(maxsplit=2)
                    if len(parts) >= 3:
                        result = self.translate(parts[2], parts[1])
                        print(f"\n?? Translation: {result}")
                    else:
                        print("Usage: /translate [lang] [text]")
                
                elif cmd.startswith("/speak "):
                    text = cmd[7:].strip()
                    if text:
                        print(f"\n?? Speaking: {text}")
                        self.speak(text)
                    else:
                        print("Usage: /speak [text]")
                
                else:
                    print("Type /help for commands")
            
            except KeyboardInterrupt:
                print("\n?? Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    LangClaw().chat()
