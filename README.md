# TimeReel

A monorepo project with Django backend and React (Vite) frontend.

## Project Structure

```
TimeReel/
├── backend/         # Django backend
│   └── core/       # Django project settings
├── frontend/       # React + Vite frontend
└── package.json    # Root package.json for managing the monorepo
```

## Setup Instructions

1. Backend Setup
   ```bash
   cd backend
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1
   # Install dependencies if not already installed
   pip install -r requirements.txt
   # Run migrations
   python manage.py migrate
   ```

2. Frontend Setup
   ```bash
   cd frontend
   npm install
   ```

3. Running the Development Servers
   ```bash
   # Run backend (from backend directory with venv activated)
   python manage.py runserver

   # In another terminal, run frontend (from frontend directory)
   npm run dev
   ```

## Development

- Backend runs on: http://localhost:8000
- Frontend runs on: http://localhost:5173

## Technologies Used

- Backend:
  - Django
  - Django REST Framework
  - Django CORS Headers

- Frontend:
  - React
  - TypeScript
  - Vite
