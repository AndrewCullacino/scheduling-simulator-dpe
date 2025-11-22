# Scheduling Simulator - Professional Edition

![Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-2.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A professional-grade real-time scheduling simulation platform. Visualize and analyze scheduling algorithms (SPT, EDF, Priority-First, DPE) with a modern interactive dashboard.

## 🚀 Quick Start

The easiest way to run the simulator is using the provided startup script.

### Option 1: One-Click Run (Recommended)
```bash
./start.sh
```
This script automatically detects your environment (Docker or Local) and launches the application.
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

### Option 2: Docker Compose
If you have Docker installed:
```bash
docker-compose up --build
```

### Option 3: Manual Setup
**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## ✨ Features

- **Interactive Dashboard**: Real-time Gantt chart visualization of task execution.
- **Algorithm Comparison**: Compare standard algorithms (SPT, EDF) with advanced research algorithms (DPE).
- **Scenario Management**: 24 built-in scenarios ranging from simple tests to extreme stress conditions.
- **Metrics Analysis**: Detailed breakdown of makespan, deadline misses, and priority handling.
- **Modern Stack**: Built with Python FastAPI and Next.js (TypeScript/Tailwind).

## 🏗 Architecture

The project follows a modern microservices architecture:

```
/
├── backend/            # FastAPI Service
│   ├── app/core/       # Simulation Engine (Python)
│   ├── app/api/        # REST Endpoints
│   └── Dockerfile
├── frontend/           # Next.js Application
│   ├── src/components/ # React Components
│   └── Dockerfile
├── docker-compose.yml  # Orchestration
└── Makefile            # Automation
```

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs) (Swagger UI)
- [Simulation Logic](backend/app/core/simulator.py)
- [Test Scenarios](backend/app/core/scenarios.py)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
