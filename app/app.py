"""
FastAPI Application Setup
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import API_TITLE, API_VERSION
from app import routes

def create_app() -> FastAPI:
    """Tạo và cấu hình FastAPI application"""
    
    app = FastAPI(title=API_TITLE, version="3.0.0")
    
    # Cấu hình CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Đăng ký routes
    app.get("/")(routes.root)
    app.get("/test-ai")(routes.test_ai_connection)
    
    # OCR
    app.post("/ocr")(routes.extract_text_from_image)
    
    # Diary & Note
    app.post("/entry")(routes.create_entry)
    app.get("/diaries")(routes.list_diaries)
    app.get("/notes")(routes.list_notes)
    
    # Reminders
    app.get("/reminders")(routes.list_reminders)
    app.put("/reminders/{reminder_id}/complete")(routes.complete_reminder)
    
    # User Profile
    app.get("/profile")(routes.get_profile)
    app.post("/profile")(routes.update_profile)
    
    # Health
    app.post("/health/log")(routes.log_health)
    app.get("/health/insights")(routes.health_insights)
    
    # AI Features
    app.get("/prompt")(routes.get_memory_prompt)
    app.post("/chat")(routes.chat)
    
    # Memory
    app.post("/memory")(routes.save_memory)
    app.get("/memories")(routes.list_memories)
    
    return app