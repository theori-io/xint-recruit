# Take-Home Assignment

A simple full-stack application with React frontend, FastAPI backend, and Redis database.

## Project Structure

```
xint-recruit/
├── frontend/              # React + TypeScript + Vite
├── backend/               # FastAPI + Python
├── compose.yaml           # Docker Compose configuration
├── README.md              # Project overview and setup
├── ASSIGNMENT.md          # Assignment instructions
├── EVALUATION_CRITERIA.md # Evaluation criteria
├── EVALUATION_GUIDE.md    # Internal Use Only
└── SOLUTION.md            # Solution template (fill this in)
```

## Features

- **Frontend**: React application with TypeScript
- **Backend**: FastAPI REST API with JWT authentication
- **Database**: Redis for data storage
- **Containerized**: Docker Compose setup for easy development

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 22+ (for local frontend development)
- Python 3.13+ (for local backend development)

### Running with Docker Compose

```bash
docker compose up
```

This will start:
- Frontend on http://localhost:3000
- Backend API on http://localhost:8000
- Redis on localhost:6379

### Running Locally

#### Backend

```bash
cd backend
uv sync  # Install dependencies
uv run python -m uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Authentication

The application uses JWT-based authentication. A default test user is created on startup:

- **Username**: `testuser`
- **Password**: `testpass123`

You can log in through the frontend interface. The authentication system is already implemented, but you may need to review and improve it as part of the assignment.

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## Assignment

See [ASSIGNMENT.md](./ASSIGNMENT.md) for complete assignment instructions.

## Evaluation

See [EVALUATION_CRITERIA.md](./EVALUATION_CRITERIA.md) for how your solution will be evaluated.
