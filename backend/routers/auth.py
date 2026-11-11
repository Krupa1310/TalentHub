from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, StudentProfile, Company
from schemas.dtos import RegisterInput, LoginInput, TokenOut, UserOut
from services.security import hash_password, verify_password, create_access_token
from services.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenOut)
def register(data: RegisterInput, db: Session = Depends(get_db)):
    role = data.role.lower().strip()
    if role not in ("student", "company"):
        raise HTTPException(status_code=400, detail="Public registration is available for student or company roles only")
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(full_name=data.full_name, email=data.email.lower(),
                password_hash=hash_password(data.password), role=role)
    db.add(user)
    db.flush()
    if role == "student":
        db.add(StudentProfile(user_id=user.id, usn=data.usn, branch=data.branch,
                              semester=data.semester, cgpa=data.cgpa))
    else:
        if not data.company_name:
            raise HTTPException(status_code=400, detail="company_name is required for company registration")
        db.add(Company(user_id=user.id, company_name=data.company_name,
                       website=data.website, industry=data.industry))
    db.commit()
    db.refresh(user)
    return {"access_token": create_access_token(user.id, user.role), "user": user}

@router.post("/login", response_model=TokenOut)
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token": create_access_token(user.id, user.role), "user": user}

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
