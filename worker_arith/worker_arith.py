from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    expression: str

@app.post("/compute")
def compute(task: Task):
    try:
        result = eval(task.expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
