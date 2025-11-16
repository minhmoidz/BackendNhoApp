"""
Memory & Diary OCR API - Main Entry Point
"""
import os
from dotenv import load_dotenv
from app.server import start_server

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    NGROK_TOKEN = os.getenv("NGROK_TOKEN", "")
    
    if not NGROK_TOKEN:
        print("\n⚠️  CẢNH BÁO: Chưa cấu hình NGROK_TOKEN trong file .env!")
        print("📝 Lấy token tại: https://dashboard.ngrok.com/get-started/your-authtoken")
        print("🔧 Server sẽ chạy mà không có Ngrok public URL.\n")
        start_server(port=8000, ngrok_token=None)
    else:
        start_server(port=8000, ngrok_token=NGROK_TOKEN)