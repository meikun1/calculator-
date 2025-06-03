from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

class Task(BaseModel):
    expression: str

@app.post("/calculate")
async def calculate(task: Task):
    if any(op in task.expression for op in ["integrate", "diff"]):
        worker_url = "http://worker_symbolic:8000/compute"
    else:
        worker_url = "http://worker_arith:8000/compute"

    async with httpx.AsyncClient() as client:
        response = await client.post(worker_url, json=task.dict())
        return response.json()
