from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False)  # student, company, coordinator
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    company_profile = relationship("Company", back_populates="user", uselist=False)

class StudentProfile(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    usn = Column(String(40), unique=True, nullable=True)
    branch = Column(String(100), nullable=True)
    semester = Column(Integer, nullable=True)
    cgpa = Column(Float, nullable=True)
    phone = Column(String(25), nullable=True)
    resume_url = Column(String(500), nullable=True)
    user = relationship("User", back_populates="student_profile")
    applications = relationship("Application", back_populates="student")

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    company_name = Column(String(160), nullable=False)
    website = Column(String(300), nullable=True)
    industry = Column(String(120), nullable=True)
    location = Column(String(160), nullable=True)
    description = Column(Text, nullable=True)
    user = relationship("User", back_populates="company_profile")
    jobs = relationship("JobListing", back_populates="company")

class JobListing(Base):
    __tablename__ = "job_listings"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String(180), nullable=False)
    description = Column(Text, nullable=False)
    job_type = Column(String(60), default="Full-time")
    location = Column(String(160), nullable=True)
    salary_lpa = Column(Float, nullable=True)
    min_cgpa = Column(Float, default=0)
    eligible_branches = Column(Text, nullable=True)  # display/cache; normalized rows below are authoritative
    deadline = Column(String(30), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    company = relationship("Company", back_populates="jobs")
    allowed_branches = relationship("JobAllowedBranch", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job")

class JobAllowedBranch(Base):
    __tablename__ = "job_allowed_branches"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_listings.id"), nullable=False)
    branch_name = Column(String(100), nullable=False)
    job = relationship("JobListing", back_populates="allowed_branches")
    __table_args__ = (UniqueConstraint("job_id", "branch_name", name="uq_job_branch"),)

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_listings.id"), nullable=False)
    status = Column(String(30), default="Applied", nullable=False)
    applied_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("StudentProfile", back_populates="applications")
    job = relationship("JobListing", back_populates="applications")
    interview = relationship("InterviewSlot", back_populates="application", uselist=False)
    offer = relationship("Offer", back_populates="application", uselist=False)
    __table_args__ = (UniqueConstraint("student_id", "job_id", name="uq_student_job_application"),)

class InterviewSlot(Base):
    __tablename__ = "interview_slots"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), unique=True, nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    mode = Column(String(30), default="Online")
    meeting_link = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    application = relationship("Application", back_populates="interview")

class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), unique=True, nullable=False)
    package_lpa = Column(Float, nullable=True)
    offer_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(30), default="Issued")
    application = relationship("Application", back_populates="offer")
