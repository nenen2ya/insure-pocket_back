from pydantic import BaseModel, Field
from typing import Optional


# =========================
# 레포트 생성용
# =========================
class ReportCreate(BaseModel):
    user_id: int = Field(..., description="레포트를 작성한 사용자 ID (FK: users.id)")
    comment: str = Field(..., max_length=1024, description="사용자 코멘트 내용")

    class Config:
        orm_mode = True


# =========================
# 응답용
# =========================
class Report(ReportCreate):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
