from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/calculate")
async def calculate(data: dict):
    try:
        expression = data.get("expression")
        if not expression:
            raise HTTPException(status_code=400, detail="Expression missing")
        result = eval(expression)  # Замените на безопасную альтернативу в продакшене
        return {"result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))