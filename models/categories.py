from pydantic import BaseModel
from typing import Optional
from enum import Enum


# =========================
# ENUM
# =========================
class CategoryType(str, Enum):
    cancer = "cancer"
    brain = "brain"
    heart = "heart"
    indemnity = "indemnity"
    dental = "dental" 
    death = "death"
    disability = "disability"
    nursing_care = "nursing_care"
    dementia = "dementia"


# =========================
# 카테고리 생성용
# =========================
class CategoryCreate(BaseModel):
    type: str

    class Config:
        orm_mode = True


# =========================
# 응답용
# =========================
class Category(CategoryCreate):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
