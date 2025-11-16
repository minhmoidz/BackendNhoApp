"""
API Routes/Endpoints - Enhanced Version
"""
from fastapi import File, UploadFile, HTTPException, Form, Body
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime
import base64
import json

from app.services.ocr_service import OCRService
from app.services.ai_service import AIService
from app.database import StorageManager

# ========== ROOT & TEST ==========

async def root():
    """Root endpoint - API Info"""
    return {
        "message": "Memory & Diary OCR API - AI Enhanced Edition",
        "version": "3.0.0",
        "ai_provider": "Groq (Llama 3)",
        "new_features": [
            "Phân biệt Diary vs Note",
            "AI phân tích ghi chú thông minh",
            "Tự động tạo nhắc nhở",
            "Quản lý hồ sơ người dùng",
            "Nhật ký sức khỏe",
            "Phân tích xu hướng sức khỏe",
            "Chat AI có ngữ cảnh"
        ],
        "endpoints": {
            "basic": {
                "ocr": "/ocr (POST)",
                "test_ai": "/test-ai (GET)"
            },
            "diary_note": {
                "create_entry": "/entry (POST) - Tạo nhật ký hoặc note",
                "list_diaries": "/diaries (GET)",
                "list_notes": "/notes (GET)"
            },
            "reminder": {
                "list_reminders": "/reminders (GET)",
                "complete_reminder": "/reminders/{id}/complete (PUT)"
            },
            "user": {
                "get_profile": "/profile (GET)",
                "update_profile": "/profile (POST)"
            },
            "health": {
                "log_health": "/health/log (POST)",
                "health_insights": "/health/insights (GET)"
            },
            "ai": {
                "memory_prompt": "/prompt (GET)",
                "chat": "/chat (POST)"
            },
            "memory": {
                "save_memory": "/memory (POST)",
                "list_memories": "/memories (GET)"
            }
        }
    }

async def test_ai_connection():
    """Test kết nối với Groq API"""
    result = await AIService.call_groq_api(
        "Chào bạn! Hãy trả lời ngắn gọn bằng tiếng Việt.",
        "Bạn là trợ lý AI."
    )
    
    if result:
        return {
            "success": True,
            "message": "Groq API hoạt động tốt!",
            "response": result
        }
    else:
        return {
            "success": False,
            "message": "Không thể kết nối Groq API. Kiểm tra GROQ_API_KEY!",
            "guide": "Lấy API key tại: https://console.groq.com/"
        }

# ========== OCR ==========

async def extract_text_from_image(file: UploadFile = File(...)):
    """Endpoint OCR cơ bản"""
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File phải là ảnh")
        
        contents = await file.read()
        extracted_text = await OCRService.extract_text_from_image(contents)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "filename": file.filename,
                "text": extracted_text,
                "length": len(extracted_text)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý ảnh: {str(e)}")

# ========== DIARY & NOTE ==========

async def create_entry(
    file: UploadFile = File(...),
    entry_type: str = Form(...),  # "diary" hoặc "note"
    auto_analyze: bool = Form(True)
):
    """
    Tạo nhật ký hoặc ghi chú từ ảnh
    - entry_type="diary": Tạo nhật ký + tóm tắt + phân tích cảm xúc
    - entry_type="note": Tạo ghi chú + phân tích thông minh + tự động tạo reminder
    """
    try:
        if entry_type not in ["diary", "note"]:
            raise HTTPException(status_code=400, detail="entry_type phải là 'diary' hoặc 'note'")
        
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File phải là ảnh")
        
        # OCR
        contents = await file.read()
        extracted_text = await OCRService.extract_text_from_image(contents)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Không đọc được text từ ảnh")
        
        image_base64 = base64.b64encode(contents).decode('utf-8')
        
        # ===== XỬ LÝ DIARY =====
        if entry_type == "diary":
            summary = None
            emotion = None
            
            if auto_analyze:
                summary = await AIService.summarize_diary(extracted_text)
                emotion = await AIService.analyze_emotion(extracted_text)
            
            diary_entry = {
                "id": f"diary_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "content": extracted_text,
                "summary": summary,
                "emotion": emotion,
                "image_base64": image_base64,
                "entry_type": "diary",
                "created_at": datetime.now().isoformat()
            }
            
            StorageManager.save_diary(diary_entry)
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "type": "diary",
                    "diary_id": diary_entry["id"],
                    "original_text": extracted_text,
                    "summary": summary,
                    "emotion": emotion,
                    "message": "Nhật ký đã được lưu!"
                }
            )
        
        # ===== XỬ LÝ NOTE =====
        else:
            # Lấy user profile để AI phân tích tốt hơn
            user_profile = StorageManager.get_user_profile()
            
            # AI phân tích note
            analysis = None
            created_reminders = []
            
            if auto_analyze:
                analysis = await AIService.analyze_note(extracted_text, user_profile)
                
                # Tạo note
                note = {
                    "id": f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "content": extracted_text,
                    "category": analysis.get('category'),
                    "extracted_datetime": analysis.get('extracted_datetime'),
                    "priority": analysis.get('priority'),
                    "is_reminder": analysis.get('should_create_reminder', False),
                    "created_at": datetime.now().isoformat()
                }
                
                StorageManager.save_note(note)
                
                # Tự động tạo reminders nếu cần
                if analysis.get('should_create_reminder'):
                    reminders = await AIService.generate_reminders_from_note(note, analysis)
                    for reminder in reminders:
                        StorageManager.save_reminder(reminder)
                        created_reminders.append(reminder)
            
            else:
                # Không phân tích, lưu note cơ bản
                note = {
                    "id": f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "content": extracted_text,
                    "category": "other",
                    "extracted_datetime": None,
                    "priority": "medium",
                    "is_reminder": False,
                    "created_at": datetime.now().isoformat()
                }
                StorageManager.save_note(note)
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "type": "note",
                    "note_id": note["id"],
                    "original_text": extracted_text,
                    "analysis": analysis,
                    "reminders_created": len(created_reminders),
                    "reminders": [
                        {
                            "id": r["id"],
                            "title": r["title"],
                            "remind_at": r["remind_at"]
                        }
                        for r in created_reminders
                    ],
                    "message": f"Ghi chú đã lưu! {'Đã tạo ' + str(len(created_reminders)) + ' nhắc nhở.' if created_reminders else ''}"
                }
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tạo entry: {str(e)}")

async def list_diaries(limit: int = 10):
    """Xem danh sách nhật ký"""
    try:
        diaries = StorageManager.get_recent_diaries(limit)
        
        for d in diaries:
            d.pop('image_base64', None)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "total": len(StorageManager.get_all_diaries()),
                "diaries": diaries
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

async def list_notes(limit: int = 10):
    """Xem danh sách ghi chú"""
    try:
        notes = StorageManager.get_recent_notes(limit)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "total": len(StorageManager.get_all_notes()),
                "notes": notes
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

# ========== REMINDERS ==========

async def list_reminders(status: str = "pending"):
    """
    Xem danh sách nhắc nhở
    - status="pending": Chưa hoàn thành
    - status="all": Tất cả
    """
    try:
        if status == "pending":
            reminders = StorageManager.get_pending_reminders()
        else:
            reminders = StorageManager.get_all_reminders()
        
        # Sắp xếp theo thời gian nhắc
        reminders = sorted(reminders, key=lambda x: x['remind_at'])
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "total": len(reminders),
                "reminders": reminders
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

async def complete_reminder(reminder_id: str):
    """Đánh dấu nhắc nhở đã hoàn thành"""
    try:
        success = StorageManager.update_reminder_status(reminder_id, True)
        
        if success:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "Đã đánh dấu hoàn thành!"
                }
            )
        else:
            raise HTTPException(status_code=404, detail="Không tìm thấy nhắc nhở")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

# ========== USER PROFILE ==========

async def get_profile():
    """Lấy thông tin người dùng"""
    try:
        profile = StorageManager.get_user_profile()
        
        if not profile:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "profile": None,
                    "message": "Chưa có thông tin người dùng"
                }
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "profile": profile
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

async def update_profile(profile_data: dict = Body(...)):
    """Cập nhật/tạo mới thông tin người dùng"""
    try:
        existing_profile = StorageManager.get_user_profile()
        
        if existing_profile:
            # Update
            profile_data['id'] = existing_profile['id']
            profile_data['created_at'] = existing_profile['created_at']
            profile_data['updated_at'] = datetime.now().isoformat()
        else:
            # Create new
            profile_data['id'] = "user_profile"
            profile_data['created_at'] = datetime.now().isoformat()
            profile_data['updated_at'] = datetime.now().isoformat()
        
        StorageManager.save_user_profile(profile_data)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "profile": profile_data,
                "message": "Đã cập nhật thông tin!"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

# ========== HEALTH ==========

async def log_health(
    log_type: str = Form(...),
    value: str = Form(...),
    note: Optional[str] = Form(None)
):
    """
    Ghi nhật ký sức khỏe
    log_type: blood_pressure, blood_sugar, weight, medication, symptom
    """
    try:
        health_log = {
            "id": f"health_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "log_type": log_type,
            "value": value,
            "note": note,
            "created_at": datetime.now().isoformat()
        }
        
        StorageManager.save_health_log(health_log)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "log_id": health_log["id"],
                "message": "Đã ghi nhận thông tin sức khỏe!"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

async def health_insights():
    """Phân tích xu hướng sức khỏe bằng AI"""
    try:
        health_logs = StorageManager.get_all_health_logs()
        
        if not health_logs:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "insights": "Chưa có dữ liệu sức khỏe để phân tích.",
                    "suggestion": "Hãy bắt đầu ghi chép các thông số sức khỏe hàng ngày!"
                }
            )
        
        user_profile = StorageManager.get_user_profile()
        insights = await AIService.analyze_health_trend(health_logs, user_profile)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "total_logs": len(health_logs),
                "insights": insights or "Không thể phân tích lúc này.",
                "recent_logs": StorageManager.get_all_health_logs()[-5:]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

# ========== AI FEATURES ==========

async def get_memory_prompt():
    """Gợi ý hồi tưởng cá nhân hóa"""
    try:
        diaries = StorageManager.get_all_diaries()
        memories = StorageManager.get_all_memories()
        user_profile = StorageManager.get_user_profile()
        
        if not diaries and not memories:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "prompt": "Chào bác! Hôm nay bác có muốn kể cho cháu nghe về kỷ niệm đẹp nào từ tuổi thơ không ạ?",
                    "note": "Chưa có dữ liệu"
                }
            )
        
        prompt_text = await AIService.generate_memory_prompt_text(diaries, memories, user_profile)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "prompt": prompt_text or "Bác có nhớ món ăn yêu thích hồi nhỏ không ạ?",
                "based_on": {
                    "diary_count": len(diaries),
                    "memory_count": len(memories),
                    "has_profile": user_profile is not None
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

async def chat(message: str = Body(..., embed=True)):
    """Chat với AI có ngữ cảnh"""
    try:
        user_profile = StorageManager.get_user_profile()
        
        # Lấy lịch sử hội thoại gần nhất
        conversations = StorageManager.get_all_conversations()
        recent_conversation = conversations[-1] if conversations else None
        
        conversation_history = []
        if recent_conversation:
            conversation_history = recent_conversation.get('messages', [])
        
        # AI chat
        response = await AIService.chat_with_context(
            message,
            conversation_history,
            user_profile
        )
        
        # Lưu hội thoại
        conversation_history.append({"role": "user", "content": message})
        conversation_history.append({"role": "assistant", "content": response})
        
        conversation = {
            "id": f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "messages": conversation_history,
            "created_at": datetime.now().isoformat()
        }
        StorageManager.save_conversation(conversation)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "response": response,
                "conversation_id": conversation["id"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

# ========== MEMORY ==========

async def save_memory(
    content: str = Form(...),
    tags: Optional[str] = Form(None)
):
    """Lưu mảnh ký ức"""
    try:
        tag_list = []
        if tags:
            tag_list = [t.strip() for t in tags.split(',')]
        
        memory = {
            "id": f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "content": content,
            "tags": tag_list,
            "created_at": datetime.now().isoformat()
        }
        
        StorageManager.save_memory(memory)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "memory_id": memory["id"],
                "message": "Ký ức đã được lưu!"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")

async def list_memories(limit: int = 10):
    """Xem danh sách ký ức"""
    try:
        memories = StorageManager.get_recent_memories(limit)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "total": len(StorageManager.get_all_memories()),
                "memories": memories
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")