from pydantic import BaseModel, Field
from typing import Optional


# =========================
# 서브카테고리 생성용
# =========================
class SubcategoryCreate(BaseModel):
    category_id: int = Field(..., description="연결된 상위 카테고리의 ID (FK)")
    name: str = Field(..., description="서브카테고리 이름")

    class Config:
        orm_mode = True


# =========================
# 응답용
# =========================
class Subcategory(SubcategoryCreate):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
