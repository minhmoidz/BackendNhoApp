"""
AI Service Layer - Groq API Integration
Các tính năng AI thông minh
"""
import aiohttp
import re
from typing import Optional, List, Dict, Tuple
from datetime import datetime, timedelta
from app.config import (
    GROQ_API_KEY, 
    GROQ_API_URL, 
    GROQ_MODEL, 
    GROQ_TEMPERATURE, 
    GROQ_MAX_TOKENS
)

class AIService:
    """Service xử lý các tác vụ AI"""
    
    @staticmethod
    async def call_groq_api(prompt: str, system_prompt: str = "") -> Optional[str]:
        """Gọi Groq API (Llama 3)"""
        try:
            if not GROQ_API_KEY:
                print("Lỗi: GROQ_API_KEY không được tìm thấy trong .env")
                return None
            
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": GROQ_TEMPERATURE,
                "max_tokens": GROQ_MAX_TOKENS
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(GROQ_API_URL, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        print(f"Groq API Error: {error_text}")
                        return None
                        
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return None
    
    # ========== DIARY & NOTE ANALYSIS ==========
    
    @staticmethod
    def generate_summary_prompt(text: str) -> str:
        """Tạo prompt tóm tắt nhật ký"""
        return f"""Bạn là trợ lý AI giúp người cao tuổi ghi chép nhật ký. 

Hãy TÓM TẮT nhật ký sau đây một cách ngắn gọn, dễ hiểu, ấm áp và có cảm xúc. 
Nên giữ lại các chi tiết quan trọng về: người, địa điểm, cảm xúc, sự kiện đặc biệt.

Nhật ký gốc:
{text}

Tóm tắt (2-3 câu ngắn gọn):"""
    
    @staticmethod
    async def summarize_diary(text: str) -> Optional[str]:
        """Tóm tắt nội dung nhật ký"""
        return await AIService.call_groq_api(
            AIService.generate_summary_prompt(text),
            "Bạn là trợ lý tóm tắt nhật ký cho người cao tuổi."
        )
    
    @staticmethod
    async def analyze_emotion(text: str) -> Optional[str]:
        """Phân tích cảm xúc từ nhật ký/ghi chú"""
        prompt = f"""Phân tích cảm xúc chính trong đoạn text sau của người cao tuổi.
Trả lời CHỈ MỘT TỪ: vui_vẻ, hạnh_phúc, buồn, lo_lắng, bình_thường, nhớ_nhung, biết_ơn, cô_đơn

Text: {text}

Cảm xúc:"""
        
        result = await AIService.call_groq_api(prompt, "Bạn là chuyên gia phân tích cảm xúc.")
        return result.strip().lower() if result else "bình_thường"
    
    # ========== NOTE INTELLIGENCE ==========
    
    @staticmethod
    async def analyze_note(content: str, user_profile: Optional[Dict] = None) -> Dict:
        """
        Phân tích thông minh nội dung ghi chú
        - Phân loại (thuốc, sự kiện, hẹn khám, công việc...)
        - Trích xuất ngày/giờ
        - Đánh giá mức độ ưu tiên
        - Đề xuất tạo nhắc nhở
        """
        
        profile_context = ""
        if user_profile:
            profile_context = f"""
Thông tin người dùng:
- Tên: {user_profile.get('full_name', 'N/A')}
- Tuổi: {user_profile.get('age', 'N/A')}
- Bệnh lý: {', '.join(user_profile.get('medical_conditions', [])) or 'Không có'}
- Thuốc đang dùng: {', '.join([m.get('name', '') for m in user_profile.get('medications', [])]) or 'Không có'}
"""
        
        prompt = f"""{profile_context}

Phân tích ghi chú sau và trả lời CHÍNH XÁC theo format JSON (không thêm text nào khác):

Ghi chú: "{content}"

{{
  "category": "medication|event|appointment|task|health|other",
  "extracted_datetime": "YYYY-MM-DD HH:MM hoặc null",
  "priority": "high|medium|low",
  "should_create_reminder": true|false,
  "reminder_suggestion": "Gợi ý tiêu đề nhắc nhở (nếu có)",
  "analysis": "Giải thích ngắn gọn"
}}"""
        
        result = await AIService.call_groq_api(
            prompt,
            "Bạn là AI phân tích ghi chú thông minh. Trả lời CHỈ JSON, không có text khác."
        )
        
        if result:
            try:
                # Loại bỏ markdown code block nếu có
                cleaned = result.strip()
                if cleaned.startswith("```"):
                    cleaned = re.sub(r'^```(?:json)?\n?', '', cleaned)
                    cleaned = re.sub(r'\n?```$', '', cleaned)
                
                import json
                return json.loads(cleaned)
            except:
                pass
        
        # Fallback
        return {
            "category": "other",
            "extracted_datetime": None,
            "priority": "medium",
            "should_create_reminder": False,
            "reminder_suggestion": None,
            "analysis": "Không thể phân tích"
        }
    
    # ========== REMINDER GENERATION ==========
    
    @staticmethod
    async def generate_reminders_from_note(note: Dict, analysis: Dict) -> List[Dict]:
        """Tạo danh sách nhắc nhở từ ghi chú"""
        reminders = []
        
        if not analysis.get('should_create_reminder'):
            return reminders
        
        extracted_dt = analysis.get('extracted_datetime')
        if not extracted_dt:
            return reminders
        
        try:
            # Parse datetime
            remind_time = datetime.fromisoformat(extracted_dt)
            
            # Tạo các nhắc nhở theo loại
            category = analysis.get('category')
            
            if category == 'medication':
                # Nhắc trước 30 phút
                reminders.append({
                    "id": f"reminder_{datetime.now().strftime('%Y%m%d_%H%M%S')}_1",
                    "note_id": note['id'],
                    "title": f"🔔 {analysis.get('reminder_suggestion', 'Uống thuốc')}",
                    "description": note['content'],
                    "remind_at": (remind_time - timedelta(minutes=30)).isoformat(),
                    "is_completed": False,
                    "created_at": datetime.now().isoformat()
                })
            
            elif category == 'appointment':
                # Nhắc trước 1 ngày và 1 giờ
                reminders.append({
                    "id": f"reminder_{datetime.now().strftime('%Y%m%d_%H%M%S')}_1",
                    "note_id": note['id'],
                    "title": f"📅 Nhắc lịch hẹn ngày mai",
                    "description": note['content'],
                    "remind_at": (remind_time - timedelta(days=1)).isoformat(),
                    "is_completed": False,
                    "created_at": datetime.now().isoformat()
                })
                reminders.append({
                    "id": f"reminder_{datetime.now().strftime('%Y%m%d_%H%M%S')}_2",
                    "note_id": note['id'],
                    "title": f"⏰ {analysis.get('reminder_suggestion', 'Chuẩn bị đi khám')}",
                    "description": note['content'],
                    "remind_at": (remind_time - timedelta(hours=1)).isoformat(),
                    "is_completed": False,
                    "created_at": datetime.now().isoformat()
                })
            
            elif category == 'event':
                # Nhắc trước 1 ngày
                reminders.append({
                    "id": f"reminder_{datetime.now().strftime('%Y%m%d_%H%M%S')}_1",
                    "note_id": note['id'],
                    "title": f"🎉 {analysis.get('reminder_suggestion', 'Sự kiện sắp diễn ra')}",
                    "description": note['content'],
                    "remind_at": (remind_time - timedelta(days=1)).isoformat(),
                    "is_completed": False,
                    "created_at": datetime.now().isoformat()
                })
            
            else:
                # Default: nhắc đúng giờ
                reminders.append({
                    "id": f"reminder_{datetime.now().strftime('%Y%m%d_%H%M%S')}_1",
                    "note_id": note['id'],
                    "title": analysis.get('reminder_suggestion', 'Nhắc nhở'),
                    "description": note['content'],
                    "remind_at": remind_time.isoformat(),
                    "is_completed": False,
                    "created_at": datetime.now().isoformat()
                })
        
        except Exception as e:
            print(f"Error generating reminders: {e}")
        
        return reminders
    
    # ========== MEMORY PROMPTS ==========
    
    @staticmethod
    def generate_memory_prompt(diaries: List[Dict], memories: List[Dict], user_profile: Optional[Dict] = None) -> str:
        """Tạo prompt gợi ý hồi tưởng có cá nhân hóa"""
        
        recent_diaries = sorted(diaries, key=lambda x: x['created_at'], reverse=True)[:3]
        diary_context = "\n".join([f"- {d.get('summary', d['content'][:100])}" for d in recent_diaries])
        
        recent_memories = sorted(memories, key=lambda x: x['created_at'], reverse=True)[:3]
        memory_context = "\n".join([f"- {m['content'][:100]}" for m in recent_memories])
        
        profile_context = ""
        if user_profile:
            hobbies = user_profile.get('hobbies', [])
            important_dates = user_profile.get('important_dates', [])
            profile_context = f"""
Thông tin cá nhân:
- Sở thích: {', '.join(hobbies) if hobbies else 'Chưa có'}
- Ngày quan trọng: {', '.join([d.get('name', '') for d in important_dates]) if important_dates else 'Chưa có'}
"""
        
        return f"""Bạn là trợ lý AI thân thiện giúp người cao tuổi gợi nhớ lại kỷ niệm.

{profile_context}

Nhật ký gần đây:
{diary_context if diary_context else "Chưa có nhật ký"}

Ký ức đã lưu:
{memory_context if memory_context else "Chưa có ký ức"}

Yêu cầu:
- Tạo MỘT câu hỏi gợi mở sâu sắc, ấm áp để khơi gợi ký ức đẹp
- Câu hỏi phải tự nhiên, thân mật như cháu hỏi ông bà
- Liên kết với thông tin cá nhân, sở thích, nhật ký gần đây
- Gợi mở về: gia đình, tuổi thơ, món ăn, địa điểm, con người...

Câu hỏi gợi nhớ:"""
    
    @staticmethod
    async def generate_memory_prompt_text(diaries: List[Dict], memories: List[Dict], user_profile: Optional[Dict] = None) -> Optional[str]:
        """Tạo câu hỏi gợi nhớ dựa trên dữ liệu"""
        return await AIService.call_groq_api(
            AIService.generate_memory_prompt(diaries, memories, user_profile),
            "Bạn là trợ lý tạo câu hỏi gợi nhớ cho người cao tuổi."
        )
    
    # ========== HEALTH INSIGHTS ==========
    
    @staticmethod
    async def analyze_health_trend(health_logs: List[Dict], user_profile: Optional[Dict] = None) -> Optional[str]:
        """Phân tích xu hướng sức khỏe"""
        
        if not health_logs:
            return None
        
        # Lấy 10 logs gần nhất
        recent_logs = sorted(health_logs, key=lambda x: x['created_at'], reverse=True)[:10]
        log_summary = "\n".join([
            f"- {log['log_type']}: {log['value']} ({log['created_at'][:10]})"
            for log in recent_logs
        ])
        
        medical_context = ""
        if user_profile and user_profile.get('medical_conditions'):
            medical_context = f"Bệnh lý hiện tại: {', '.join(user_profile['medical_conditions'])}"
        
        prompt = f"""{medical_context}

Dữ liệu sức khỏe gần đây:
{log_summary}

Hãy phân tích xu hướng sức khỏe và đưa ra lời khuyên ngắn gọn (2-3 câu), thân thiện, dễ hiểu cho người cao tuổi.
Nếu thấy dấu hiệu bất thường, khuyên nên gặp bác sĩ."""
        
        return await AIService.call_groq_api(
            prompt,
            "Bạn là trợ lý sức khỏe AI, không phải bác sĩ, chỉ đưa ra lời khuyên tham khảo."
        )
    
    # ========== CONVERSATIONAL AI ==========
    
    @staticmethod
    async def chat_with_context(
        user_message: str,
        conversation_history: List[Dict],
        user_profile: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Chat AI với ngữ cảnh
        - Nhớ lịch sử hội thoại
        - Biết thông tin người dùng
        """
        
        profile_context = ""
        if user_profile:
            profile_context = f"""
Thông tin người dùng:
- Tên: {user_profile.get('full_name', 'N/A')}
- Tuổi: {user_profile.get('age', 'N/A')}
- Sở thích: {', '.join(user_profile.get('hobbies', [])) or 'Chưa rõ'}
"""
        
        history_text = ""
        if conversation_history:
            history_text = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in conversation_history[-5:]  # 5 tin nhắn gần nhất
            ])
        
        prompt = f"""{profile_context}

Lịch sử hội thoại:
{history_text if history_text else "Đây là cuộc trò chuyện mới"}

Tin nhắn hiện tại: {user_message}

Hãy trả lời thân thiện, ấm áp như một người cháu đang trò chuyện với ông bà."""
        
        return await AIService.call_groq_api(
            prompt,
            "Bạn là trợ lý AI thân thiện, hỗ trợ người cao tuổi. Luôn lịch sự, kiên nhẫn và dễ hiểu."
        )