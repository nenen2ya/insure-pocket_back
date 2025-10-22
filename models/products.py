from pydantic import BaseModel, Field
from typing import Optional


# =========================
# 상품 생성용
# =========================
class ProductCreate(BaseModel):
    company_id: int = Field(..., description="연결된 회사의 ID (FK)")
    product_name: str = Field(..., description="상품명")
    keyword1: Optional[str] = None
    summary1: Optional[str] = None
    keyword2: Optional[str] = None
    summary2: Optional[str] = None
    keyword3: Optional[str] = None
    summary3: Optional[str] = None
    keyword4: Optional[str] = None
    summary4: Optional[str] = None
    monthly_premium: Optional[float] = Field(0, ge=0, description="월 보험료 (0 이상)")

    class Config:
        orm_mode = True


# =========================
# 응답용
# =========================
class Product(ProductCreate):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
