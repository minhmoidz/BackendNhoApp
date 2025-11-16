"""
Data Models
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DiaryEntry(BaseModel):
    id: str
    content: str
    summary: Optional[str] = None
    image_base64: Optional[str] = None
    created_at: str
    entry_type: str = "diary"  # "diary" or "note"
    emotion: Optional[str] = None  # AI phân tích cảm xúc

class Memory(BaseModel):
    id: str
    content: str
    tags: List[str] = []
    created_at: str

class Note(BaseModel):
    id: str
    content: str
    category: Optional[str] = None  # "medication", "event", "appointment", "task", "other"
    extracted_datetime: Optional[str] = None  # AI trích xuất thời gian
    priority: Optional[str] = None  # "high", "medium", "low"
    is_reminder: bool = False
    created_at: str

class Reminder(BaseModel):
    id: str
    note_id: str
    title: str
    description: str
    remind_at: str  # ISO datetime
    is_completed: bool = False
    created_at: str

class UserProfile(BaseModel):
    id: str = "user_profile"
    full_name: Optional[str] = None
    age: Optional[int] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_conditions: List[str] = []  # Bệnh lý
    medications: List[dict] = []  # Danh sách thuốc đang dùng
    allergies: List[str] = []  # Dị ứng
    hobbies: List[str] = []  # Sở thích
    important_dates: List[dict] = []  # Ngày quan trọng (sinh nhật con cháu, kỷ niệm...)
    daily_routine: Optional[str] = None  # Thói quen hàng ngày
    created_at: str
    updated_at: str

class HealthLog(BaseModel):
    id: str
    log_type: str  # "blood_pressure", "blood_sugar", "weight", "medication", "symptom"
    value: str
    note: Optional[str] = None
    created_at: str

class Conversation(BaseModel):
    id: str
    messages: List[dict]  # [{"role": "user/assistant", "content": "..."}]
    created_at: str