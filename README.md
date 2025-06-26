Distributed Calculator and Image Inversion Application
Overview
This is a distributed application built with FastAPI, Docker, and React, featuring a calculator and an image inversion tool. The system is designed to handle symbolic and arithmetic calculations, as well as image processing, using a microservices architecture.
Features
Calculator: Supports symbolic (e.g., sin(x)) and arithmetic (e.g., 2^3) expressions.
Image Inversion: Inverts colors of uploaded images (JPEG/PNG) using distributed processing.
Distributed Architecture: Utilizes api, dispatcher, and worker_image services for scalability.
System Architecture
API: Handles incoming requests, distributes image segments, and performs calculations.
Dispatcher: Routes calculation requests to worker_arith or worker_symbolic and image segments to worker_image.
Worker Services:
worker_arith: Processes arithmetic calculations.
worker_symbolic: Processes symbolic calculations.
worker_image: Inverts image segments.
Frontend: React-based UI with Tailwind CSS for a modern design.
Prerequisites
Docker and Docker Compose
Node.js and npm (for frontend)
Python 3.9
Installation
1) Clone the repository:
git clone https://github.com/ваш_пользователь/distributed_calculator_fastapi.git

cd distributed_calculator_fastapi

2) Build and start the services:

docker-compose down --rmi all

docker system prune -a --volumes

docker-compose build --no-cache

docker-compose up -d


3) Install frontend dependencies and start the app:

cd frontend

npm install

npm start

Usage
Open http://localhost:3001 in your browser.
Calculator: Enter an expression (e.g., 2^3 or sin(x)) and click "Рассчитать".
Image Inversion: Drag and drop an image (JPEG/PNG) or click to upload, then click "Инвертировать цвета".
Configuration
Edit docker-compose.yml to adjust ports or replicas.
Update requirements.txt in each service directory if additional dependencies are needed.
Troubleshooting
Error 500: Check logs with docker-compose logs api, docker-compose logs dispatcher, docker-compose logs worker_image.
Network Issues: Ensure all services are running (docker-compose ps).
Image Format: Use JPEG images for best compatibility.
Contributing
Fork the repository.
Create a branch: git checkout -b feature-branch.
Commit changes: git commit -m "Add new feature".
Push to the branch: git push origin feature-branch.
Submit a pull request.
License
This project is licensed under the MIT License.
Contact
For issues or questions, contact brailov.99@mail.ru