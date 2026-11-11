from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import JobListing, JobAllowedBranch, Company
from schemas.dtos import JobCreate
from services.dependencies import require_role

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

def serialize_job(job):
    return {
        "id": job.id, "title": job.title, "description": job.description,
        "job_type": job.job_type, "location": job.location,
        "salary_lpa": job.salary_lpa, "min_cgpa": job.min_cgpa,
        "deadline": job.deadline, "company_name": job.company.company_name,
        "eligible_branches": [b.branch_name for b in job.allowed_branches]
    }

@router.get("")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobListing).filter(JobListing.is_active == True).order_by(JobListing.created_at.desc()).all()
    return [serialize_job(job) for job in jobs]

@router.post("")
def create_job(data: JobCreate, user=Depends(require_role("company")), db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.user_id == user.id).first()
    if not company:
        raise HTTPException(status_code=400, detail="Company profile not found")
    job = JobListing(company_id=company.id, title=data.title, description=data.description,
                     job_type=data.job_type, location=data.location, salary_lpa=data.salary_lpa,
                     min_cgpa=data.min_cgpa, deadline=data.deadline,
                     eligible_branches=", ".join(data.eligible_branches))
    db.add(job)
    db.flush()
    for branch in sorted(set(x.strip() for x in data.eligible_branches if x.strip())):
        db.add(JobAllowedBranch(job_id=job.id, branch_name=branch))
    db.commit()
    db.refresh(job)
    return serialize_job(job)

@router.get("/mine")
def my_jobs(user=Depends(require_role("company")), db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.user_id == user.id).first()
    jobs = db.query(JobListing).filter(JobListing.company_id == company.id).all()
    return [serialize_job(job) for job in jobs]
