from fastapi import FastAPI
from pydantic import BaseModel
import base64
from PIL import Image
import io
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class SegmentRequest(BaseModel):
    data: str
    start_y: int
    height: int

class SegmentResponse(BaseModel):
    inverted_data: str

@app.post("/process_segment")
async def process_segment(request: SegmentRequest) -> SegmentResponse:
    if not request.data:
        logger.warning("Empty segment data received")
        return SegmentResponse(inverted_data="")
    try:
        logger.info(f"Decoding segment at {request.start_y}")
        img_data = base64.b64decode(request.data)
        img = Image.open(io.BytesIO(img_data))
        if img.mode != 'RGB':
            logger.info(f"Converting image at {request.start_y} from {img.mode} to RGB")
            img = img.convert('RGB')
        img_array = np.array(img, dtype=np.uint8)
        if img_array.size == 0:
            raise ValueError("Empty image array")
        logger.info(f"Inverting segment at {request.start_y}, shape: {img_array.shape}")
        inverted_array = 255 - img_array
        inverted_img = Image.fromarray(inverted_array, mode='RGB')
        buffered = io.BytesIO()
        inverted_img.save(buffered, format="JPEG", quality=95)
        return SegmentResponse(inverted_data=base64.b64encode(buffered.getvalue()).decode('utf-8'))
    except Exception as e:
        logger.error(f"Error processing segment at {request.start_y}: {e}")
        return SegmentResponse(inverted_data="")