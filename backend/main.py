from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal
import models  # registers SQLAlchemy models before create_all
from models import User
from services.security import hash_password
from routers import auth, jobs, applications, dashboard

app = FastAPI(
    title="TalentHub API",
    description="Campus Placement Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        coordinator_email = "coordinator@talenthub.local"
        if not db.query(User).filter(User.email == coordinator_email).first():
            db.add(User(
                full_name="TalentHub Coordinator",
                email=coordinator_email,
                password_hash=hash_password("Admin@12345"),
                role="coordinator"
            ))
            db.commit()
    finally:
        db.close()

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return {"message": "Welcome to TalentHub Backend!", "status": "Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
