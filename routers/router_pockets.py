from fastapi import APIRouter
from models.pockets import Pocket, PocketCreate

from db import supabase

router = APIRouter(prefix="/pockets")

@router.get("/{user.id}")
def get_users():
    try:
        response = supabase.table("users").select("*").execute()
        return response.data
    except Exception as e:
        import traceback
        traceback.print_exc()  # 콘솔에 에러 전체 출력
        return {"error": str(e)}


