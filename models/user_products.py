from pydantic import BaseModel, Field
from typing import Optional


# =========================
# 사용자-상품 연결 생성용
# =========================
class UserProductCreate(BaseModel):
    user_id: int = Field(..., description="연결된 사용자 ID (FK: users.id)")
    product_id: int = Field(..., description="연결된 상품 ID (FK: products.id)")

    class Config:
        orm_mode = True


# =========================
# 응답용
# =========================
class UserProduct(UserProductCreate):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
