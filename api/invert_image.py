from fastapi import FastAPI
from pydantic import BaseModel
import base64
from PIL import Image
import io
import requests
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class ImageRequest(BaseModel):
    image: str

class ImageResponse(BaseModel):
    inverted_image: str

def distribute_segments(image_data: str, segment_count: int = 10) -> List[dict]:
    try:
        logger.info("Decoding base64 image data")
        img_data = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_data))
        width, height = img.size
        segment_height = height // segment_count
        segments = []
        for i in range(segment_count):
            start_y = i * segment_height
            end_y = start_y + segment_height if i < 9 else height
            segment = img.crop((0, start_y, width, end_y))
            buffered = io.BytesIO()
            segment.save(buffered, format="JPEG", quality=95)
            segments.append({
                "data": base64.b64encode(buffered.getvalue()).decode('utf-8'),
                "start_y": start_y,
                "height": end_y - start_y
            })
        logger.info(f"Distributed {len(segments)} segments")
        return segments
    except Exception as e:
        logger.error(f"Error in distribute_segments: {e}")
        return []

def process_segments(segments: List[dict]) -> List[dict]:
    inverted_segments = []
    for segment in segments:
        try:
            logger.info(f"Sending segment to dispatcher: {segment}")
            response = requests.post("http://dispatcher:8000/process_segment", json=segment, timeout=10)
            response.raise_for_status()
            inverted_segments.append({"data": response.json()["inverted_data"], "start_y": segment["start_y"], "height": segment["height"]})
        except Exception as e:
            logger.error(f"Error processing segment: {e}")
            inverted_segments.append({"data": segment["data"], "start_y": segment["start_y"], "height": segment["height"]})
    return inverted_segments

@app.post("/invert_image")
async def invert_image(request: ImageRequest) -> ImageResponse:
    logger.info("Received invert_image request")
    segments = distribute_segments(request.image)
    if not segments:
        logger.error("No segments generated")
        return ImageResponse(inverted_image=request.image)

    inverted_segments = process_segments(segments)
    if not inverted_segments:
        logger.error("No inverted segments processed")
        return ImageResponse(inverted_image=request.image)

    try:
        img = Image.new('RGB', (Image.open(io.BytesIO(base64.b64decode(request.image))).size))
        for segment in sorted(inverted_segments, key=lambda x: x["start_y"]):
            if segment["data"] and not segment["data"].startswith("Error"):
                segment_img = Image.open(io.BytesIO(base64.b64decode(segment["data"])))
                img.paste(segment_img, (0, segment["start_y"]))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=95)
        inverted_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        logger.info("Image inversion completed successfully")
        return ImageResponse(inverted_image=inverted_image)
    except Exception as e:
        logger.error(f"Error assembling inverted image: {e}")
        return ImageResponse(inverted_image=request.image)

@app.post("/calculate")
async def calculate(expression: dict) -> dict:
    try:
        result = sympy.sympify(expression["expression"].replace('^', '**'))
        return {"result": str(result)}
    except Exception as e:
        return {"result": f"Ошибка: {str(e)}"}