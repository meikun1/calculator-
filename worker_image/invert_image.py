from fastapi import FastAPI
from pydantic import BaseModel
import base64
from PIL import Image
import io
import numpy as np
from typing import List
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class ImageRequest(BaseModel):
    image: str

class ImageResponse(BaseModel):
    inverted_image: str

def invert_image_segment(segment_data: str, start_y: int, height: int) -> str:
    try:
        logger.info("Decoding segment data")
        img_data = base64.b64decode(segment_data)
        img = Image.open(io.BytesIO(img_data))
        img_array = np.array(img)
        inverted_array = 255 - img_array
        inverted_img = Image.fromarray(inverted_array)
        buffered = io.BytesIO()
        inverted_img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error inverting segment at {start_y}: {e}")
        return segment_data  # Возвращаем оригинал при ошибке

@app.post("/invert_image")
async def invert_image(request: ImageRequest) -> ImageResponse:
    logger.info("Received invert_image request")
    try:
        # Декодируем исходное изображение
        logger.info("Decoding base64 image data")
        img_data = base64.b64decode(request.image)
        img = Image.open(io.BytesIO(img_data))
        width, height = img.size
        
        # Разбиваем на 10 сегментов по вертикали
        segment_height = height // 10
        segments = []
        for i in range(10):
            start_y = i * segment_height
            end_y = start_y + segment_height if i < 9 else height
            segment = img.crop((0, start_y, width, end_y))
            buffered = io.BytesIO()
            segment.save(buffered, format="JPEG")
            segments.append({
                "data": base64.b64encode(buffered.getvalue()).decode('utf-8'),
                "start_y": start_y,
                "height": end_y - start_y
            })
        
        # Инвертируем сегменты
        logger.info(f"Processing {len(segments)} segments")
        inverted_segments = []
        for segment in segments:
            inverted_segment = invert_image_segment(segment["data"], segment["start_y"], segment["height"])
            inverted_segments.append({"data": inverted_segment, "start_y": segment["start_y"], "height": segment["height"]})
        
        # Собираем изображение обратно
        final_img = Image.new('RGB', (width, height))
        for segment in sorted(inverted_segments, key=lambda x: x["start_y"]):
            logger.info(f"Pasting segment at {segment['start_y']}")
            segment_img = Image.open(io.BytesIO(base64.b64decode(segment["data"])))
            if segment_img.size[0] != width or segment_img.size[1] != segment["height"]:
                logger.warning(f"Segment size mismatch at {segment['start_y']}: expected ({width}, {segment['height']}), got {segment_img.size}")
            final_img.paste(segment_img, (0, segment["start_y"]))
        
        # Конвертируем в base64
        buffered = io.BytesIO()
        final_img.save(buffered, format="JPEG")
        inverted_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        logger.info("Image inversion completed successfully")
        return ImageResponse(inverted_image=inverted_image)
    except Exception as e:
        logger.error(f"Error in invert_image: {e}")
        return ImageResponse(inverted_image=request.image)  # Возвращаем оригинал при ошибке

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)