import httpx

while True:
    expr = input("Введите выражение (или 'exit'): ")
    if expr == "exit":
        break

    response = httpx.post("http://localhost:8000/calculate", json={"expression": expr})
    print("Ответ:", response.json())
