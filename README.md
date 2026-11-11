# TalentHub – Campus Placement Management System

A runnable starter MVP using React + Vite, FastAPI, SQLAlchemy and SQLite.

## Features
- Student and company registration/login
- Role-based access (student, company, coordinator)
- Student profile and company profile records
- Company job posting and public job browsing
- Student job applications
- Company view of applicants and update application status
- Coordinator overview statistics
- SQLite database created automatically at first backend startup
- Swagger API documentation

## Requirements
- Python 3.10+
- Node.js 20+
- npm

## 1. Backend setup (PowerShell)
Open a terminal in `TalentHub\backend`:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Backend:
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### Demo coordinator account
- Email: `coordinator@talenthub.local`
- Password: `Admin@12345`

Change the demo password before using this beyond local development.

## 2. Frontend setup
Open a second terminal in `TalentHub\frontend`:

```powershell
npm install
npm run dev
```

Frontend: http://localhost:5173

## Database
SQLite file is created as `backend/talenthub.db`. To reset the local demo database, stop the backend and delete this file. The tables will be recreated on next startup.

## Important
This is an educational MVP, not a production deployment. Before production use, configure a strong secret key, HTTPS, migrations, email verification, password reset, rate limiting, audit logging and proper deployment secrets.
