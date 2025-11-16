Memory & Diary OCR API - AI Enhanced Edition
API thông minh hỗ trợ người cao tuổi ghi chép nhật ký, quản lý ghi chú, tự động nhắc nhở và chăm sóc sức khỏe.
✨ Tính năng mới (Version 3.0)
🎯 Core Features

✅ Phân biệt Diary vs Note: Người dùng có thể chọn viết nhật ký hoặc ghi chú quan trọng
✅ AI Phân tích thông minh: Tự động phân loại, trích xuất thời gian, đánh giá mức độ quan trọng
✅ Tự động tạo nhắc nhở: AI đề xuất và tạo reminder dựa trên nội dung ghi chú
✅ Quản lý hồ sơ người dùng: Lưu thông tin cá nhân, bệnh lý, thuốc đang dùng
✅ Nhật ký sức khỏe: Theo dõi huyết áp, đường huyết, cân nặng...
✅ AI Phân tích sức khỏe: Nhận diện xu hướng và đưa ra lời khuyên
✅ Chat AI có ngữ cảnh: Trò chuyện thân thiện, nhớ lịch sử và thông tin người dùng

🤖 AI Intelligence

Phân tích cảm xúc từ nhật ký
Tóm tắt nội dung tự động
Phân loại ghi chú (thuốc, hẹn khám, sự kiện...)
Trích xuất ngày giờ từ văn bản tự nhiên
Gợi ý hồi tưởng cá nhân hóa
Phân tích xu hướng sức khỏe

📁 Cấu trúc thư mục
project/
│
├── main.py                          # Entry point
├── requirements.txt                 # Dependencies
├── .env                            # Environment variables
├── .env.example                    # Template
├── README.md                       # Documentation
│
├── app/
│   ├── __init__.py
│   ├── config.py                   # Cấu hình
│   ├── models.py                   # Data models
│   ├── database.py                 # Storage layer
│   ├── routes.py                   # API endpoints
│   ├── app.py                      # FastAPI setup
│   ├── server.py                   # Server startup
│   │
│   └── services/
│       ├── __init__.py
│       ├── ai_service.py           # AI Intelligence
│       └── ocr_service.py          # OCR
│
└── storage/                        # Data storage
    ├── diaries.json
    ├── notes.json
    ├── reminders.json
    ├── memories.json
    ├── user_profile.json
    ├── health_logs.json
    └── conversations.json
🚀 Cài đặt nhanh
1. Install dependencies
bashpip install -r requirements.txt
2. Install Tesseract OCR

Windows: https://github.com/UB-Mannheim/tesseract/wiki
Linux: sudo apt install tesseract-ocr tesseract-ocr-vie
Mac: brew install tesseract tesseract-lang

3. Setup .env
bashcp .env.example .env
# Chỉnh sửa .env và thêm GROQ_API_KEY
4. Run
bashpython main.py
📚 API Documentation
🔹 Basic
Test AI
bashGET /test-ai
OCR Image
bashPOST /ocr
Content-Type: multipart/form-data

file: <image_file>

🔹 Diary & Note
Create Entry (Nhật ký hoặc Ghi chú)
bashPOST /entry
Content-Type: multipart/form-data

file: <image_file>
entry_type: "diary" | "note"
auto_analyze: true
Response khi entry_type="diary":
json{
  "success": true,
  "type": "diary",
  "diary_id": "diary_20250116_143022",
  "original_text": "...",
  "summary": "AI tóm tắt ngắn gọn",
  "emotion": "vui_vẻ"
}
Response khi entry_type="note":
json{
  "success": true,
  "type": "note",
  "note_id": "note_20250116_143022",
  "original_text": "Ngày 20/1 uống thuốc huyết áp lúc 8h sáng",
  "analysis": {
    "category": "medication",
    "extracted_datetime": "2025-01-20T08:00:00",
    "priority": "high",
    "should_create_reminder": true,
    "reminder_suggestion": "Uống thuốc huyết áp"
  },
  "reminders_created": 1,
  "reminders": [
    {
      "id": "reminder_...",
      "title": "🔔 Uống thuốc huyết áp",
      "remind_at": "2025-01-20T07:30:00"
    }
  ]
}
List Diaries
bashGET /diaries?limit=10
List Notes
bashGET /notes?limit=10

🔹 Reminders
List Reminders
bashGET /reminders?status=pending
# status: "pending" (chưa hoàn thành) hoặc "all"
Response:
json{
  "success": true,
  "total": 3,
  "reminders": [
    {
      "id": "reminder_...",
      "note_id": "note_...",
      "title": "🔔 Uống thuốc huyết áp",
      "description": "Ngày 20/1 uống thuốc...",
      "remind_at": "2025-01-20T07:30:00",
      "is_completed": false
    }
  ]
}
Complete Reminder
bashPUT /reminders/{reminder_id}/complete

🔹 User Profile
Get Profile
bashGET /profile
Update Profile
bashPOST /profile
Content-Type: application/json

{
  "full_name": "Nguyễn Văn A",
  "age": 68,
  "birth_date": "1957-03-15",
  "address": "123 Đường ABC, Hà Nội",
  "phone": "0123456789",
  "emergency_contact": "Con trai: 0987654321",
  "medical_conditions": ["Cao huyết áp", "Tiểu đường"],
  "medications": [
    {
      "name": "Thuốc huyết áp",
      "dosage": "1 viên/ngày",
      "time": "8:00 sáng"
    }
  ],
  "allergies": ["Penicillin"],
  "hobbies": ["Đọc sách", "Làm vườn"],
  "important_dates": [
    {
      "name": "Sinh nhật con trai",
      "date": "2025-05-10"
    }
  ],
  "daily_routine": "Dậy 6h, tập thể dục, ăn sáng 7h..."
}

🔹 Health
Log Health Data
bashPOST /health/log
Content-Type: multipart/form-data

log_type: "blood_pressure" | "blood_sugar" | "weight" | "medication" | "symptom"
value: "120/80"
note: "Sau khi uống thuốc"
Get Health Insights (AI Analysis)
bashGET /health/insights
Response:
json{
  "success": true,
  "total_logs": 15,
  "insights": "Huyết áp của bác trong tuần qua ổn định, dao động 120-130/80-85. Đây là dấu hiệu tốt! Hãy tiếp tục duy trì chế độ ăn uống và uống thuốc đúng giờ nhé.",
  "recent_logs": [...]
}

🔹 AI Features
Get Memory Prompt (Gợi ý hồi tưởng)
bashGET /prompt
Response:
json{
  "success": true,
  "prompt": "Bác ơi, hôm qua bác có đi chơi vườn phải không ạ? Bác có nhớ khu vườn nào mà bác thích nhất hồi còn trẻ không?",
  "based_on": {
    "diary_count": 5,
    "memory_count": 3,
    "has_profile": true
  }
}
Chat with AI
bashPOST /chat
Content-Type: application/json

{
  "message": "Hôm nay cháu cảm thấy hơi mệt"
}
Response:
json{
  "success": true,
  "response": "Ông/bà ơi, nghe ông/bà nói vậy cháu lo lắm. Ông/bà có uống đủ nước chưa ạ? Hay là ông/bà ngủ không ngon? Nếu mệt nhiều thì nên gặp bác sĩ để kiểm tra nhé!",
  "conversation_id": "conv_..."
}

🔹 Memory
Save Memory
bashPOST /memory
Content-Type: multipart/form-data

content: "Hồi bé tôi thường được bà nấu chè đậu xanh..."
tags: "gia_đình, món_ăn, tuổi_thơ"
List Memories
bashGET /memories?limit=10

🎯 Use Cases
1️⃣ Ghi nhật ký hàng ngày
User: Chụp ảnh trang nhật ký viết tay
App: POST /entry với entry_type="diary"
Result: Nhật ký được OCR, tóm tắt, phân tích cảm xúc
2️⃣ Nhắc uống thuốc
User: Chụp ảnh ghi chú "Ngày 20/1 uống thuốc lúc 8h sáng"
App: POST /entry với entry_type="note"
AI: Phân tích → Tạo reminder tự động lúc 7:30 sáng
App: Kiểm tra GET /reminders → So sánh thời gian → Hiển thị thông báo
3️⃣ Nhắc lịch hẹn khám
User: Ghi chú "Khám bệnh 25/1 lúc 9h tại BV Bạch Mai"
AI: Tạo 2 reminders:
  - 24/1: "Nhắc lịch hẹn ngày mai"
  - 25/1 lúc 8h: "Chuẩn bị đi khám"
4️⃣ Theo dõi sức khỏe
User: Ghi huyết áp hàng ngày
App: POST /health/log
Result: AI phân tích xu hướng, cảnh báo nếu bất thường
5️⃣ Gợi ý hồi tưởng
App: Lấy thông tin từ profile, nhật ký, ký ức
AI: Tạo câu hỏi gợi nhớ cá nhân hóa
Example: "Bác có nhớ món ăn yêu thích ở quê nhà không?"

🔧 Tích hợp vào Mobile App
Logic nhắc nhở trong app:
javascript// 1. Lấy danh sách reminders
const reminders = await fetch('/reminders?status=pending').then(r => r.json());

// 2. So sánh thời gian
const now = new Date();
reminders.reminders.forEach(reminder => {
  const remindTime = new Date(reminder.remind_at);
  
  if (remindTime <= now) {
    // Hiển thị notification
    showNotification(reminder.title, reminder.description);
  }
});

// 3. Khi user hoàn thành
await fetch(`/reminders/${reminder.id}/complete`, { method: 'PUT' });
Cron job (chạy mỗi 15 phút):
javascriptsetInterval(checkReminders, 15 * 60 * 1000);

🚀 Mở rộng Database
File app/database.py dễ dàng thay thế backend:
PostgreSQL
pythonclass PostgreSQLStorage(StorageManager):
    def __init__(self, conn_string):
        self.conn = psycopg2.connect(conn_string)
    
    def get_all_notes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        return cursor.fetchall()
MongoDB
pythonclass MongoDBStorage(StorageManager):
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client['memory_diary']
    
    def get_all_notes(self):
        return list(self.db.notes.find())

🎨 Ví dụ Flow hoàn chỉnh
1. User setup profile:
   POST /profile với thông tin cá nhân

2. User viết note:
   POST /entry với "Ngày 20/1 uống thuốc lúc 8h"
   → AI tự động tạo reminder

3. App kiểm tra reminders:
   GET /reminders?status=pending
   → So sánh thời gian hiện tại
   → Hiển thị thông báo nếu đến giờ

4. User hoàn thành:
   PUT /reminders/{id}/complete

5. User viết diary:
   POST /entry với "Hôm nay đi chơi công viên..."
   → AI tóm tắt + phân tích cảm xúc

6. App gợi ý:
   GET /prompt
   → AI tạo câu hỏi dựa trên diary + profile

7. User chat:
   POST /chat với "Tôi cảm thấy lo lắng"
   → AI trả lời ấm áp, có ngữ cảnh

📝 Notes

Tất cả API đều trả về JSON
Thời gian sử dụng ISO 8601 format
Hỗ trợ tiếng Việt đầy đủ
AI responses luôn thân thiện, dễ hiểu

📞 Support

API Docs: http://localhost:8000/docs
Groq API: https://console.groq.com/
Tesseract: https://github.com/tesseract-ocr/tesseract

📄 License
MIT License
