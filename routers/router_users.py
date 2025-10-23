from fastapi import APIRouter, HTTPException
from models.users import UserLogin, UserResponse
from db import supabase

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserResponse)
def login(user: UserLogin):
    # 1️⃣ Supabase에서 닉네임으로 유저 조회
    res = (
        supabase
        .table("users")
        .select("id, nickname, password, user_name")
        .eq("nickname", user.nickname)
        .execute()
    )

    if not res.data:
        raise HTTPException(status_code=404, detail="존재하지 않는 닉네임입니다.")

    db_user = res.data[0]

    # 2️⃣ 평문 비밀번호 비교
    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

    # 3️⃣ 로그인 성공 시 유저 정보 반환
    return {
        "id": db_user["id"],
        "nickname": db_user["nickname"],
        "user_name": db_user["user_name"],
    }


# router = APIRouter(prefix="/users")

# @router.get("/")
# def get_users():
#     try:
#         response = supabase.table("users").select("*").execute()
#         return response.data
#     except Exception as e:
#         import traceback
#         traceback.print_exc()  # 콘솔에 에러 전체 출력
#         return {"error": str(e)}


# @router.get("/{user_id}")
# def read_user(user_id: int):
#     try:
#         response = (
#             supabase.table("users")
#             .select("id, nickname, user_name, gender, age, job, drinking, smoking, drive_license")
#             .eq("id", user_id)
#             .single()  # 단일 행 반환
#             .execute()
#         )

#         if not response.data:
#             return print(status_code=404, content={"error": "User not found"})
        
#         return {"user": response.data}

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return print(status_code=500, content={"error": str(e)})
    


