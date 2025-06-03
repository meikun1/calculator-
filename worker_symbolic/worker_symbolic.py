from fastapi import FastAPI
from pydantic import BaseModel
from sympy import sympify, integrate, diff

app = FastAPI()

class Task(BaseModel):
    expression: str

@app.post("/compute")
def compute(task: Task):
    try:
        expr = sympify(task.expression)
        if "integrate" in task.expression:
            result = integrate(expr)
        elif "diff" in task.expression:
            result = diff(expr)
        else:
            result = expr.evalf()
        return {"result": str(result)}
    except Exception as e:
        return {"error": str(e)}
