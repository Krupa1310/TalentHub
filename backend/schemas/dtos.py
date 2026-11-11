from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterInput(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8)
    role: str
    usn: Optional[str] = None
    branch: Optional[str] = None
    semester: Optional[int] = None
    cgpa: Optional[float] = None
    company_name: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class JobCreate(BaseModel):
    title: str
    description: str
    job_type: str = "Full-time"
    location: Optional[str] = None
    salary_lpa: Optional[float] = None
    min_cgpa: float = 0
    eligible_branches: List[str] = []
    deadline: Optional[str] = None

class JobOut(BaseModel):
    id: int
    title: str
    description: str
    job_type: str
    location: Optional[str]
    salary_lpa: Optional[float]
    min_cgpa: float
    deadline: Optional[str]
    company_name: str
    eligible_branches: List[str]
    model_config = ConfigDict(from_attributes=True)

class StatusUpdate(BaseModel):
    status: str

class InterviewCreate(BaseModel):
    scheduled_at: datetime
    mode: str = "Online"
    meeting_link: Optional[str] = None
    notes: Optional[str] = None

class OfferCreate(BaseModel):
    package_lpa: Optional[float] = None
