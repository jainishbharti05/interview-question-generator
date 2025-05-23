from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ExperienceLevel(str, Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"

class Domain(str, Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    WEB_DEVELOPMENT = "web_development"
    DATA_SCIENCE = "data_science"

class Question(BaseModel):
    question: str
    difficulty: int = Field(..., ge=1, le=10)
    skill_area: str
    evaluation_criteria: List[str]
    example_answer: Optional[str] = None

class QuestionRequest(BaseModel):
    job_requirements: List[str]
    experience_level: ExperienceLevel
    domain: Domain
    num_questions: Optional[int] = 1

class QuestionResponse(BaseModel):
    questions: List[Question]
