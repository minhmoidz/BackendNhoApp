"""
Server Startup & Configuration
"""
import uvicorn
from pyngrok import ngrok
import nest_asyncio
from app.app import create_app
from app.config import GROQ_API_KEY

# Cho phép chạy uvicorn trong môi trường async
nest_asyncio.apply()

def start_server(port: int = 8000, ngrok_token: str = None):
    """
    Khởi động server FastAPI với Ngrok
    
    Args:
        port: Cổng chạy server (default: 8000)
        ngrok_token: Token ngrok để tạo public URL
    """
    try:
        # Kiểm tra API key
        if not GROQ_API_KEY:
            print("\n⚠️  CẢNH BÁO: Chưa cấu hình GROQ_API_KEY trong file .env!")
            print("📝 Lấy API key tại: https://console.groq.com/")
        
        # Tạo FastAPI app
        app = create_app()
        
        # Ngrok setup
        public_url = None
        if ngrok_token:
            ngrok.set_auth_token(ngrok_token)
            public_url = ngrok.connect(port)
        
        # Print server info
        print(f"\n{'='*70}")
        print(f"🚀 Server đang chạy tại: http://localhost:{port}")
        
        if public_url:
            print(f"🌐 Public URL (Ngrok): {public_url}")
            print(f"🤖 AI Provider: Groq (Llama 3)")
            print(f"\n📚 API Endpoints:")
            print(f"   • Test AI:          {public_url}/test-ai")
            print(f"   • OCR ảnh:          {public_url}/ocr")
            print(f"   • Tạo nhật ký:      {public_url}/diary")
            print(f"   • Lưu ký ức:        {public_url}/memory")
            print(f"   • Gợi ý hồi tưởng:  {public_url}/prompt")
            print(f"   • API Docs:         {public_url}/docs")
        else:
            print("🌐 Ngrok: Bị tắt (không tìm thấy NGROK_TOKEN trong .env)")
            print(f"🤖 AI Provider: Groq (Llama 3)")
            print(f"   • API Docs (local): http://localhost:{port}/docs")
        
        print(f"{'='*70}\n")
        
        # Start server
        uvicorn.run(app, host="0.0.0.0", port=port)
        
    except Exception as e:
        print(f"❌ Lỗi server: {e}")
