from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import StudentProfile, JobListing, Application, Company
from schemas.dtos import StatusUpdate, InterviewCreate, OfferCreate
from services.dependencies import require_role

router = APIRouter(prefix="/api", tags=["Applications and Placement"])

@router.post("/jobs/{job_id}/apply")
def apply(job_id: int, user=Depends(require_role("student")), db: Session = Depends(get_db)):
    student = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    job = db.query(JobListing).filter(JobListing.id == job_id, JobListing.is_active == True).first()
    if not student or not job:
        raise HTTPException(status_code=404, detail="Student profile or job not found")
    if student.cgpa is not None and student.cgpa < (job.min_cgpa or 0):
        raise HTTPException(status_code=400, detail="Your CGPA does not meet this job's minimum requirement")
    branches = [b.branch_name.lower() for b in job.allowed_branches]
    if branches and student.branch and student.branch.lower() not in branches:
        raise HTTPException(status_code=400, detail="Your branch is not eligible for this job")
    if db.query(Application).filter_by(student_id=student.id, job_id=job.id).first():
        raise HTTPException(status_code=409, detail="You have already applied")
    app = Application(student_id=student.id, job_id=job.id)
    db.add(app)
    db.commit()
    return {"message": "Application submitted successfully", "application_id": app.id}

@router.get("/applications/mine")
def my_applications(user=Depends(require_role("student")), db: Session = Depends(get_db)):
    student = db.query(StudentProfile).filter_by(user_id=user.id).first()
    apps = db.query(Application).filter_by(student_id=student.id).order_by(Application.applied_at.desc()).all()
    return [{"id": a.id, "job_title": a.job.title, "company": a.job.company.company_name,
             "status": a.status, "applied_at": a.applied_at.isoformat()} for a in apps]

@router.get("/company/applications")
def company_applications(user=Depends(require_role("company")), db: Session = Depends(get_db)):
    company = db.query(Company).filter_by(user_id=user.id).first()
    jobs = db.query(JobListing).filter_by(company_id=company.id).all()
    result = []
    for job in jobs:
        for a in job.applications:
            result.append({"id": a.id, "job_id": job.id, "job_title": job.title,
                           "student_name": a.student.user.full_name, "email": a.student.user.email,
                           "branch": a.student.branch, "cgpa": a.student.cgpa, "status": a.status})
    return result

@router.patch("/applications/{application_id}/status")
def update_status(application_id: int, data: StatusUpdate,
                  user=Depends(require_role("company", "coordinator")), db: Session = Depends(get_db)):
    allowed = {"Under Review", "Shortlisted", "Rejected", "Selected"}
    if data.status not in allowed:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {', '.join(sorted(allowed))}")
    app = db.query(Application).filter_by(id=application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if user.role == "company":
        company = db.query(Company).filter_by(user_id=user.id).first()
        if app.job.company_id != company.id:
            raise HTTPException(status_code=403, detail="This application does not belong to your company")
    app.status = data.status
    db.commit()
    return {"message": "Application status updated", "status": app.status}

@router.post("/applications/{application_id}/interview")
def schedule_interview(application_id: int, data: InterviewCreate,
                       user=Depends(require_role("company", "coordinator")), db: Session = Depends(get_db)):
    app = db.query(Application).filter_by(id=application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if user.role == "company":
        company = db.query(Company).filter_by(user_id=user.id).first()
        if app.job.company_id != company.id:
            raise HTTPException(status_code=403, detail="Not your company's application")
    if app.interview:
        raise HTTPException(status_code=409, detail="Interview already scheduled for this application")
    from models import InterviewSlot
    slot = InterviewSlot(application_id=app.id, scheduled_at=data.scheduled_at,
                         mode=data.mode, meeting_link=data.meeting_link, notes=data.notes)
    db.add(slot)
    app.status = "Shortlisted"
    db.commit()
    return {"message": "Interview scheduled", "interview_id": slot.id}

@router.post("/applications/{application_id}/offer")
def issue_offer(application_id: int, data: OfferCreate,
                user=Depends(require_role("company", "coordinator")), db: Session = Depends(get_db)):
    app = db.query(Application).filter_by(id=application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if user.role == "company":
        company = db.query(Company).filter_by(user_id=user.id).first()
        if app.job.company_id != company.id:
            raise HTTPException(status_code=403, detail="Not your company's application")
    if app.offer:
        raise HTTPException(status_code=409, detail="Offer already exists")
    from models import Offer
    offer = Offer(application_id=app.id, package_lpa=data.package_lpa)
    db.add(offer)
    app.status = "Selected"
    db.commit()
    return {"message": "Offer issued", "offer_id": offer.id}
