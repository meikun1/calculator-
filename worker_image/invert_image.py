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
        return SegmentResponse(inverted_data="")
    try:
        logger.info(f"Processing segment at {request.start_y}")
        img_data = base64.b64decode(request.data)
        img = Image.open(io.BytesIO(img_data))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_array = np.array(img, dtype=np.uint8)
        inverted_array = 255 - img_array
        inverted_img = Image.fromarray(inverted_array, mode='RGB')
        buffered = io.BytesIO()
        inverted_img.save(buffered, format="JPEG", quality=95)
        return SegmentResponse(inverted_data=base64.b64encode(buffered.getvalue()).decode('utf-8'))
    except Exception as e:
        logger.error(f"Error processing segment: {e}")
        return SegmentResponse(inverted_data=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)