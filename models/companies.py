from pydantic import BaseModel
from typing import Optional


# =========================
# 회사 생성용
# =========================
class CompanyCreate(BaseModel):
    company_name: str
    url: str


# =========================
# 응답용
# =========================
class Company(CompanyCreate):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
