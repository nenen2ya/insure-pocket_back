from pydantic import BaseModel, Field
from typing import Optional


# =========================
# 개인화 권장 보장금액 생성용
# =========================
class UserResultCreate(BaseModel):
    user_id: int = Field(..., description="사용자 ID (FK: users.id)")
    subcategory_id: int = Field(..., description="서브카테고리 ID (FK: subcategories.id)")
    recommended_coverage: int = Field(
        0, ge=0, description="권장 보장 금액 (0 이상, 기본값 0)"
    )

    class Config:
        orm_mode = True


# =========================
# 응답용
# =========================
class UserResult(UserResultCreate):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
