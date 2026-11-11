# TalentHub – Campus Placement Management System

**TalentHub** is a web-based Campus Placement Management System designed to simplify and manage the placement process between students, companies, and placement coordinators.

The platform provides a centralized system for student registration, company job postings, job applications, and placement coordination.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Installation and Setup](#installation-and-setup)
6. [Running the Application](#running-the-application)
7. [API Documentation](#api-documentation)
8. [Database](#database)
9. [Future Enhancements](#future-enhancements)

---

## 1. Project Overview

TalentHub aims to digitize the campus placement process by connecting students, companies, and placement coordinators through a single platform.

Students can create profiles and apply for available job opportunities. Companies can register, publish job openings, view applicants, and manage application statuses. Coordinators can monitor placement activities through an overview dashboard.

## 2. Features

### Student Module
- Student registration and login.
- Student profile management.
- Browse available job opportunities.
- Apply for company job openings.
- Track job application status.

### Company Module
- Company registration and login.
- Company profile management.
- Create and publish job openings.
- View student applications.
- Update application statuses.

### Coordinator Module
- Coordinator login.
- Overview of placement activities.
- Dashboard statistics.

### General Features
- Role-based access for students, companies, and coordinators.
- REST API integration.
- Automatic SQLite database creation.
- Interactive Swagger API documentation.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js |
| Build Tool | Vite |
| Backend | Python, FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| API Documentation | Swagger UI |
| Package Management | npm, pip |

## 4. Project Structure

```text
TalentHub/
│
├── backend/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## 5. Installation and Setup

### Prerequisites

- Python 3.10 or higher
- Node.js 20 or higher
- npm

### Backend Setup

Open PowerShell and navigate to the backend directory:

```powershell
cd backend

py -m venv venv

.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt
```

If PowerShell blocks virtual environment activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\venv\Scripts\Activate.ps1
```

### Frontend Setup

Open a second terminal:

```powershell
cd frontend

npm install
```

## 6. Running the Application

### Start Backend

From the backend directory:

```powershell
uvicorn main:app --reload --port 8000
```

Backend URL:

http://127.0.0.1:8000

### Start Frontend

From the frontend directory:

```powershell
npm run dev
```

Frontend URL:

http://localhost:5173

## 7. API Documentation

TalentHub uses FastAPI to provide REST APIs.

Swagger UI documentation is available at:

http://127.0.0.1:8000/docs

Health Check:

http://127.0.0.1:8000/health

## 8. Database

TalentHub uses SQLite with SQLAlchemy ORM for database operations.

- Database: SQLite
- ORM: SQLAlchemy
- Database file: `backend/talenthub.db`
- The database is created automatically when the backend starts.

To reset the local demo database, stop the backend and delete `backend/talenthub.db`. The tables will be recreated on the next startup.

## 9. Future Enhancements

- Resume upload and management.
- Advanced job search and filtering.
- Email notifications for application updates.
- Placement analytics and reporting.
- Interview scheduling.
- Improved authentication and security.


---

*TalentHub – Connecting Students, Companies, and Opportunities.*
