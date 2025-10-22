from pydantic import BaseModel, Field
from typing import Optional


# =========================
# 찜(pocket) 생성용
# =========================
class PocketCreate(BaseModel):
    user_id: int = Field(..., description="찜한 사용자 ID (FK: users.id)")
    product_id: int = Field(..., description="찜한 상품 ID (FK: products.id)")

    class Config:
        orm_mode = True


# =========================
# 응답용
# =========================
class Pocket(PocketCreate):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
