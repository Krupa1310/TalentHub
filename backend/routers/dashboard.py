from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import User, StudentProfile, Company, JobListing, Application, Offer
from services.dependencies import require_role

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/coordinator")
def coordinator_dashboard(user=Depends(require_role("coordinator")), db: Session = Depends(get_db)):
    return {
        "students": db.query(func.count(StudentProfile.id)).scalar() or 0,
        "companies": db.query(func.count(Company.id)).scalar() or 0,
        "active_jobs": db.query(func.count(JobListing.id)).filter(JobListing.is_active == True).scalar() or 0,
        "applications": db.query(func.count(Application.id)).scalar() or 0,
        "offers": db.query(func.count(Offer.id)).scalar() or 0
    }

@router.get("/student")
def student_dashboard(user=Depends(require_role("student")), db: Session = Depends(get_db)):
    student = db.query(StudentProfile).filter_by(user_id=user.id).first()
    total = db.query(func.count(Application.id)).filter_by(student_id=student.id).scalar() or 0
    return {"name": user.full_name, "branch": student.branch, "cgpa": student.cgpa, "applications": total}

@router.get("/company")
def company_dashboard(user=Depends(require_role("company")), db: Session = Depends(get_db)):
    company = db.query(Company).filter_by(user_id=user.id).first()
    jobs = db.query(func.count(JobListing.id)).filter_by(company_id=company.id).scalar() or 0
    return {"company": company.company_name, "jobs_posted": jobs}
