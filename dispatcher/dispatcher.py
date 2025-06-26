from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import re
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_symbolic_expression(expression: str) -> bool:
    """Определяет, является ли выражение символическим (содержит x, sin, cos, ∫, sqrt)."""
    symbolic_patterns = [r'x', r'sin', r'cos', r'∫', r'sqrt']
    return any(re.search(pattern, expression, re.IGNORECASE) for pattern in symbolic_patterns)

# Используем общий сервис worker_image (Docker Compose автоматически балансирует)
WORKER_IMAGE_URL = "http://worker_image:8000/process_segment"

@app.post("/calculate")
async def calculate(data: dict):
    try:
        expression = data.get("expression")
        if not expression:
            raise HTTPException(status_code=400, detail="Expression missing")
        
        if is_symbolic_expression(expression):
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://worker_symbolic:8000/calculate",
                    json={"expression": expression}
                )
                response.raise_for_status()
                return response.json()
        else:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://worker_arith:8000/calculate",
                    json={"expression": expression}
                )
                response.raise_for_status()
                return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e.response.text))
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/process_segment")
async def process_segment(segment: dict):
    try:
        logger.info(f"Forwarding segment to {WORKER_IMAGE_URL}")
        async with httpx.AsyncClient() as client:
            response = await client.post(WORKER_IMAGE_URL, json=segment, timeout=10)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error forwarding to {WORKER_IMAGE_URL}: {e}")
        return {"inverted_data": segment["data"]}
    except httpx.RequestError as e:
        logger.error(f"Request error forwarding to {WORKER_IMAGE_URL}: {e}")
        return {"inverted_data": segment["data"]}
    except Exception as e:
        logger.error(f"Unexpected error forwarding to {WORKER_IMAGE_URL}: {e}")
        return {"inverted_data": segment["data"]}