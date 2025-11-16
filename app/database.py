"""
Database/Storage Layer
Tách riêng để dễ dàng thay thế bằng PostgreSQL, MongoDB, etc.
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.config import (
    DIARY_FILE, MEMORY_FILE, NOTE_FILE, REMINDER_FILE, 
    USER_PROFILE_FILE, HEALTH_LOG_FILE, CONVERSATION_FILE
)

class StorageManager:
    """
    Quản lý lưu trữ dữ liệu
    Hiện tại: JSON file
    Tương lai: Có thể thay thế bằng database khác
    """
    
    @staticmethod
    def load_json_file(file_path: Path) -> List[Dict[str, Any]]:
        """Đọc dữ liệu từ file JSON"""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    @staticmethod
    def save_json_file(file_path: Path, data: List[Dict[str, Any]]):
        """Lưu dữ liệu vào file JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ========== DIARY OPERATIONS ==========
    
    @staticmethod
    def get_all_diaries() -> List[Dict[str, Any]]:
        """Lấy tất cả nhật ký"""
        return StorageManager.load_json_file(DIARY_FILE)
    
    @staticmethod
    def save_diary(diary: Dict[str, Any]) -> bool:
        """Lưu một nhật ký mới"""
        try:
            diaries = StorageManager.get_all_diaries()
            diaries.append(diary)
            StorageManager.save_json_file(DIARY_FILE, diaries)
            return True
        except Exception as e:
            print(f"Error saving diary: {e}")
            return False
    
    @staticmethod
    def get_recent_diaries(limit: int = 10) -> List[Dict[str, Any]]:
        """Lấy nhật ký gần nhất"""
        diaries = StorageManager.get_all_diaries()
        return sorted(diaries, key=lambda x: x['created_at'], reverse=True)[:limit]
    
    # ========== MEMORY OPERATIONS ==========
    
    @staticmethod
    def get_all_memories() -> List[Dict[str, Any]]:
        """Lấy tất cả ký ức"""
        return StorageManager.load_json_file(MEMORY_FILE)
    
    @staticmethod
    def save_memory(memory: Dict[str, Any]) -> bool:
        """Lưu một ký ức mới"""
        try:
            memories = StorageManager.get_all_memories()
            memories.append(memory)
            StorageManager.save_json_file(MEMORY_FILE, memories)
            return True
        except Exception as e:
            print(f"Error saving memory: {e}")
            return False
    
    @staticmethod
    def get_recent_memories(limit: int = 10) -> List[Dict[str, Any]]:
        """Lấy ký ức gần nhất"""
        memories = StorageManager.get_all_memories()
        return sorted(memories, key=lambda x: x['created_at'], reverse=True)[:limit]
    
    # ========== NOTE OPERATIONS ==========
    
    @staticmethod
    def get_all_notes() -> List[Dict[str, Any]]:
        """Lấy tất cả ghi chú"""
        return StorageManager.load_json_file(NOTE_FILE)
    
    @staticmethod
    def save_note(note: Dict[str, Any]) -> bool:
        """Lưu ghi chú mới"""
        try:
            notes = StorageManager.get_all_notes()
            notes.append(note)
            StorageManager.save_json_file(NOTE_FILE, notes)
            return True
        except Exception as e:
            print(f"Error saving note: {e}")
            return False
    
    @staticmethod
    def get_recent_notes(limit: int = 10) -> List[Dict[str, Any]]:
        """Lấy ghi chú gần nhất"""
        notes = StorageManager.get_all_notes()
        return sorted(notes, key=lambda x: x['created_at'], reverse=True)[:limit]
    
    # ========== REMINDER OPERATIONS ==========
    
    @staticmethod
    def get_all_reminders() -> List[Dict[str, Any]]:
        """Lấy tất cả nhắc nhở"""
        return StorageManager.load_json_file(REMINDER_FILE)
    
    @staticmethod
    def save_reminder(reminder: Dict[str, Any]) -> bool:
        """Lưu nhắc nhở mới"""
        try:
            reminders = StorageManager.get_all_reminders()
            reminders.append(reminder)
            StorageManager.save_json_file(REMINDER_FILE, reminders)
            return True
        except Exception as e:
            print(f"Error saving reminder: {e}")
            return False
    
    @staticmethod
    def get_pending_reminders() -> List[Dict[str, Any]]:
        """Lấy các nhắc nhở chưa hoàn thành"""
        reminders = StorageManager.get_all_reminders()
        return [r for r in reminders if not r.get('is_completed', False)]
    
    @staticmethod
    def update_reminder_status(reminder_id: str, is_completed: bool) -> bool:
        """Cập nhật trạng thái nhắc nhở"""
        try:
            reminders = StorageManager.get_all_reminders()
            for r in reminders:
                if r['id'] == reminder_id:
                    r['is_completed'] = is_completed
            StorageManager.save_json_file(REMINDER_FILE, reminders)
            return True
        except Exception as e:
            print(f"Error updating reminder: {e}")
            return False
    
    # ========== USER PROFILE OPERATIONS ==========
    
    @staticmethod
    def get_user_profile() -> Optional[Dict[str, Any]]:
        """Lấy thông tin người dùng"""
        profiles = StorageManager.load_json_file(USER_PROFILE_FILE)
        return profiles[0] if profiles else None
    
    @staticmethod
    def save_user_profile(profile: Dict[str, Any]) -> bool:
        """Lưu/cập nhật thông tin người dùng"""
        try:
            StorageManager.save_json_file(USER_PROFILE_FILE, [profile])
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    # ========== HEALTH LOG OPERATIONS ==========
    
    @staticmethod
    def get_all_health_logs() -> List[Dict[str, Any]]:
        """Lấy tất cả nhật ký sức khỏe"""
        return StorageManager.load_json_file(HEALTH_LOG_FILE)
    
    @staticmethod
    def save_health_log(log: Dict[str, Any]) -> bool:
        """Lưu nhật ký sức khỏe"""
        try:
            logs = StorageManager.get_all_health_logs()
            logs.append(log)
            StorageManager.save_json_file(HEALTH_LOG_FILE, logs)
            return True
        except Exception as e:
            print(f"Error saving health log: {e}")
            return False
    
    # ========== CONVERSATION OPERATIONS ==========
    
    @staticmethod
    def get_all_conversations() -> List[Dict[str, Any]]:
        """Lấy tất cả hội thoại"""
        return StorageManager.load_json_file(CONVERSATION_FILE)
    
    @staticmethod
    def save_conversation(conversation: Dict[str, Any]) -> bool:
        """Lưu hội thoại"""
        try:
            conversations = StorageManager.get_all_conversations()
            conversations.append(conversation)
            StorageManager.save_json_file(CONVERSATION_FILE, conversations)
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False


# ========== FUTURE: DATABASE IMPLEMENTATIONS ==========

class PostgreSQLStorage(StorageManager):
    """
    Ví dụ: Triển khai với PostgreSQL
    Uncomment và sử dụng khi cần
    """
    pass
    # def __init__(self, connection_string: str):
    #     self.conn = psycopg2.connect(connection_string)
    
    # def get_all_diaries(self):
    #     cursor = self.conn.cursor()
    #     cursor.execute("SELECT * FROM diaries ORDER BY created_at DESC")
    #     return cursor.fetchall()


class MongoDBStorage(StorageManager):
    """
    Ví dụ: Triển khai với MongoDB
    """
    pass
    # def __init__(self, mongo_uri: str):
    #     self.client = MongoClient(mongo_uri)
    #     self.db = self.client['memory_diary']
    
    # def get_all_diaries(self):
    #     return list(self.db.diaries.find())