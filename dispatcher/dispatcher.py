from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import re

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

@app.post("/calculate")
async def calculate(data: dict):
    try:
        expression = data.get("expression")
        if not expression:
            raise HTTPException(status_code=400, detail="Expression missing")
        
        # Определяем тип выражения
        if is_symbolic_expression(expression):
            # Отправляем в worker_symbolic
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://worker_symbolic:8000/calculate",
                    json={"expression": expression}
                )
                response.raise_for_status()
                return response.json()
        else:
            # Отправляем в worker_arith
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