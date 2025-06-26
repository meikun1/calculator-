from fastapi import FastAPI, HTTPException
from sympy import sympify, integrate, sqrt, sin, cos, Symbol, pi
import re

app = FastAPI()

def parse_integral(expression: str):
    """Парсит выражение интеграла вида ∫(f(x), x)."""
    match = re.match(r'∫\((.*),\s*([a-zA-Z])\)$', expression)
    if match:
        func, var = match.groups()
        return func.strip(), var.strip()
    return None, None

def check_brackets(expression: str) -> bool:
    """Проверяет, закрыты ли все скобки."""
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

@app.post("/calculate")
async def calculate(data: dict):
    try:
        expression = data.get("expression")
        if not expression:
            raise HTTPException(status_code=400, detail="Expression missing")
        
        # Проверка скобок
        if not check_brackets(expression):
            raise HTTPException(status_code=400, detail="'(' was never closed")

        x = Symbol('x')
        # Безопасный namespace для sympify
        safe_namespace = {
            'sqrt': sqrt,
            'sin': sin,
            'cos': cos,
            'pi': pi,
            'x': x
        }

        # Проверяем, является ли выражение интегралом
        func, var = parse_integral(expression)
        if func and var:
            expr = sympify(func, locals=safe_namespace)
            result = integrate(expr, x)
        else:
            expr = sympify(expression, locals=safe_namespace)
            result = expr.evalf() if expr.is_number else expr
        
        return {"result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))