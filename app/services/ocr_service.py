"""
OCR Service Layer
"""
import pytesseract
from PIL import Image
import io
from app.config import TESSERACT_CMD

# Cấu hình Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

class OCRService:
    """Service xử lý OCR"""
    
    @staticmethod
    async def extract_text_from_image(image_bytes: bytes) -> str:
        """
        Trích xuất text từ ảnh
        
        Args:
            image_bytes: Dữ liệu ảnh dạng bytes
            
        Returns:
            Text đã trích xuất
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            extracted_text = pytesseract.image_to_string(image, lang='vie+eng')
            return extracted_text.strip()
        except Exception as e:
            raise Exception(f"Lỗi OCR: {str(e)}")