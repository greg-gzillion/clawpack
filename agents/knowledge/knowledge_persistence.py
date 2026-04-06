# knowledge_persistence.py - Prevent Knowledge Loss
import sqlite3
import json
import shutil
from pathlib import Path
from datetime import datetime
# Shared memory integration for Knowledge Agent
import sqlite3
from pathlib import Path

class SharedMemory:
    def __init__(self):
        self.db_path = Path.home() / ".claw_memory" / "shared_memory.db"
    
    def get_all_knowledge(self):
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            
            # Get all tables data
            result = {}
            tables = ['medical_knowledge', 'translations', 'math_knowledge', 'language_vocab', 'tx_knowledge']
            for table in tables:
                try:
                    c.execute(f'SELECT COUNT(*) FROM {table}')
                    result[table] = c.fetchone()[0]
                except:
                    result[table] = 0
            
            conn.close()
            return result
        except:
            return {}, timedelta
import os

class KnowledgePersistence:
    def __init__(self):
        self.shared_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.backup_path = Path.home() / ".claw_memory" / "backups"
        self.archive_path = Path.home() / ".claw_memory" / "archive"
        self.init_system()
    
    def init_system(self):
        """Initialize persistence system"""
        self.backup_path.mkdir(parents=True, exist_ok=True)
        self.archive_path.mkdir(parents=True, exist_ok=True)
        
        # Create audit log for all knowledge changes
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT,
                record_id INTEGER,
                action TEXT,
                old_value TEXT,
                new_value TEXT,
                timestamp TEXT,
                agent TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT UNIQUE,
                metric_value TEXT,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Knowledge Persistence System initialized")
    
    def backup(self, backup_name=None):
        """Create a backup of all knowledge"""
        if not backup_name:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_file = self.backup_path / f"{backup_name}.db"
        
        # Copy the database
        shutil.copy2(self.shared_path, backup_file)
        
        # Compress backup
        import zipfile
        zip_path = self.backup_path / f"{backup_name}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(backup_file, arcname=f"{backup_name}.db")
        
        # Remove uncompressed backup
        backup_file.unlink()
        
        # Log the backup
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO knowledge_metrics (metric_name, metric_value, timestamp)
            VALUES (?, ?, ?)
        """, (f"backup_{backup_name}", zip_path.name, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        print(f"✅ Backup created: {zip_path}")
        return zip_path
    
    def consolidate_knowledge(self):
        """Deduplicate and consolidate knowledge"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        # Find duplicate medical knowledge
        cursor.execute("""
            SELECT query, COUNT(*), GROUP_CONCAT(id)
            FROM medical_knowledge
            GROUP BY query
            HAVING COUNT(*) > 1
        """)
        
        duplicates = cursor.fetchall()
        
        for query, count, ids in duplicates:
            id_list = ids.split(',')
            keep_id = id_list[0]
            delete_ids = id_list[1:]
            
            print(f"Consolidating '{query[:50]}...' ({count} duplicates)")
            
            # Merge usage counts
            cursor.execute(f"""
                UPDATE medical_knowledge 
                SET usage_count = usage_count + (
                    SELECT SUM(usage_count) FROM medical_knowledge 
                    WHERE id IN ({','.join(delete_ids)})
                )
                WHERE id = {keep_id}
            """)
            
            # Delete duplicates
            cursor.execute(f"DELETE FROM medical_knowledge WHERE id IN ({','.join(delete_ids)})")
        
        conn.commit()
        conn.close()
        print(f"✅ Consolidated {len(duplicates)} duplicate entries")
    
    def archive_old_knowledge(self, days_threshold=90):
        """Archive knowledge not used in X days"""
        threshold_date = (datetime.now() - timedelta(days=days_threshold)).isoformat()
        
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        # Find old medical knowledge
        cursor.execute("""
            SELECT * FROM medical_knowledge 
            WHERE timestamp < ? AND usage_count < 3
        """, (threshold_date,))
        
        old_records = cursor.fetchall()
        
        if old_records:
            # Save to archive
            archive_file = self.archive_path / f"archive_{datetime.now().strftime('%Y%m%d')}.json"
            
            if archive_file.exists():
                with open(archive_file, 'r') as f:
                    archive_data = json.load(f)
            else:
                archive_data = []
            
            for record in old_records:
                archive_data.append({
                    'table': 'medical_knowledge',
                    'record': record,
                    'archived_date': datetime.now().isoformat()
                })
            
            with open(archive_file, 'w') as f:
                json.dump(archive_data, f, indent=2)
            
            # Delete from active database
            cursor.execute("""
                DELETE FROM medical_knowledge 
                WHERE timestamp < ? AND usage_count < 3
            """, (threshold_date,))
            
            conn.commit()
            print(f"✅ Archived {len(old_records)} old records to {archive_file}")
        
        conn.close()
    
    def restore_from_backup(self, backup_file):
        """Restore knowledge from backup"""
        backup_path = self.backup_path / backup_file
        
        if not backup_path.exists():
            print(f"❌ Backup not found: {backup_path}")
            return False
        
        # Create restore point of current state
        current_backup = self.backup("pre_restore")
        
        # Restore backup
        shutil.copy2(backup_path, self.shared_path)
        
        print(f"✅ Restored from backup: {backup_file}")
        print(f"⚠️ Pre-restore state saved to: {current_backup}")
        return True
    
    def export_knowledge(self, format='json'):
        """Export all knowledge to external format"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        export_data = {}
        
        # Export all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            export_data[table_name] = {
                'columns': columns,
                'rows': rows
            }
        
        conn.close()
        
        if format == 'json':
            export_file = self.archive_path / f"knowledge_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(export_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            print(f"✅ Exported to: {export_file}")
            return export_file
        
        return export_data
    
    def get_knowledge_health(self):
        """Check health of knowledge base"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        health = {}
        
        # Check table sizes
        cursor.execute("SELECT COUNT(*) FROM medical_knowledge")
        health['medical_entries'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM translations")
        health['translation_entries'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tx_knowledge")
        health['tx_entries'] = cursor.fetchone()[0]
        
        # Check for missing data
        cursor.execute("""
            SELECT COUNT(*) FROM medical_knowledge 
            WHERE response IS NULL OR response = ''
        """)
        health['empty_responses'] = cursor.fetchone()[0]
        
        # Check backup age
        backups = list(self.backup_path.glob("*.zip"))
        if backups:
            latest_backup = max(backups, key=lambda x: x.stat().st_mtime)
            backup_age = datetime.now() - datetime.fromtimestamp(latest_backup.stat().st_mtime)
            health['latest_backup'] = f"{backup_age.days} days ago"
        else:
            health['latest_backup'] = "No backups found"
        
        conn.close()
        return health
    
    def auto_maintenance(self):
        """Run automatic maintenance"""
        print("\n🔧 Running Knowledge Maintenance...")
        
        # 1. Consolidate duplicates
        self.consolidate_knowledge()
        
        # 2. Archive old knowledge (90+ days unused)
        self.archive_old_knowledge(90)
        
        # 3. Create weekly backup
        if datetime.now().weekday() == 0:  # Monday
            self.backup("weekly_auto")
        
        # 4. Export monthly snapshot
        if datetime.now().day == 1:  # First of month
            self.export_knowledge()
        
        print("✅ Maintenance complete")
    
    def interactive_menu(self):
        """Interactive menu for knowledge management"""
        while True:
            print("\n" + "="*60)
            print("🔒 KNOWLEDGE PERSISTENCE SYSTEM")
            print("="*60)
            
            health = self.get_knowledge_health()
            print(f"\n📊 KNOWLEDGE HEALTH:")
            print(f"  Medical entries: {health['medical_entries']}")
            print(f"  Translation entries: {health['translation_entries']}")
            print(f"  TX entries: {health['tx_entries']}")
            print(f"  Empty responses: {health['empty_responses']}")
            print(f"  Latest backup: {health['latest_backup']}")
            
            print("\n📋 COMMANDS:")
            print("  1. Create backup")
            print("  2. Restore from backup")
            print("  3. Consolidate duplicates")
            print("  4. Export knowledge")
            print("  5. Run maintenance")
            print("  6. View backups")
            print("  7. Exit")
            
            choice = input("\n> ").strip()
            
            if choice == '1':
                name = input("Backup name (optional): ").strip()
                self.backup(name if name else None)
            
            elif choice == '2':
                backups = list(self.backup_path.glob("*.zip"))
                if backups:
                    print("\nAvailable backups:")
                    for i, b in enumerate(backups):
                        print(f"  {i+1}. {b.name}")
                    idx = input("Select backup number: ").strip()
                    try:
                        self.restore_from_backup(backups[int(idx)-1].name)
                    except:
                        print("Invalid selection")
                else:
                    print("No backups found")
            
            elif choice == '3':
                self.consolidate_knowledge()
            
            elif choice == '4':
                self.export_knowledge()
            
            elif choice == '5':
                self.auto_maintenance()
            
            elif choice == '6':
                backups = list(self.backup_path.glob("*.zip"))
                print("\n📚 BACKUPS:")
                for b in backups:
                    size = b.stat().st_size / 1024
                    print(f"  {b.name} ({size:.1f} KB)")
            
            elif choice == '7':
                break

if __name__ == "__main__":
    keeper = KnowledgePersistence()
    keeper.interactive_menu()