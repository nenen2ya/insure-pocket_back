from pydantic import BaseModel, Field
from typing import Optional


# =========================
# 커버리지 생성용
# =========================
class CoverageCreate(BaseModel):
    product_id: int = Field(..., description="연결된 상품의 ID (FK)")
    subcategory_id: int = Field(..., description="연결된 서브카테고리의 ID (FK)")
    coverage_amount: int = Field(
        0, ge=0, description="보장 금액 (0 이상, 기본값 0)"
    )

    class Config:
        orm_mode = True


# =========================
# 응답용
# =========================
class Coverage(CoverageCreate):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
