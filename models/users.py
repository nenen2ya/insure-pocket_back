from pydantic import BaseModel
from typing import Optional
import enum


# ------------------------------
# ENUM 타입 정의 (DB ENUM과 매핑)
# ------------------------------
class GenderType(enum.Enum):
    Male = "Male"
    Female = "Female"


class JobType(enum.Enum):
    low = "low"
    high = "high"


class DrinkingType(enum.Enum):
    none = "none"
    weekly_3 = "weekly_3"
    weekly_4_plus = "weekly_4_plus"


class SmokingType(enum.Enum):
    none = "none"
    less_than_10 = "less_than_10"
    more_than_10 = "more_than_10"


class DriverLicenseType(enum.Enum):
    YES = "YES"
    NO = "NO"

# 로그인 요청 받을 때 쓸 모델
class UserLogin(BaseModel):
    nickname: str
    password: str

# 로그인 성공 시 클라이언트로 돌려줄 데이터
class UserResponse(BaseModel):
    id: int
    nickname: str
    user_name: str

# ---------------------------------------------------
# # 유저 생성용
# class UserCreate(BaseModel):
#     nickname: str
#     password: str
#     user_name: str
#     gender: Optional[GenderType] = None
#     age: Optional[int] = None
#     job: Optional[JobType] = None
#     drinking: Optional[DrinkingType] = None
#     smoking: Optional[SmokingType] = None
#     drive_license: Optional[DriverLicenseType] = None


# # 응답용
# class User(UserCreate):
#     id: int
#     created_at: Optional[str] = None
#     updated_at: Optional[str] = None

#     class Config:
#         orm_mode = True

