from fastapi import APIRouter, HTTPException
from models.users import UserLogin, UserResponse
from db import supabase


router = APIRouter(prefix="/users")

@router.get("/")
def get_users():
    try:
        response = supabase.table("users").select("*").execute()
        return response.data
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


@router.get("/{user_id}")
def read_user(user_id: int):
    try:
        response = (
            supabase.table("users")
            .select("id, nickname, user_name, gender, age, job, drinking, smoking, drive_license")
            .eq("id", user_id)
            .single()
            .execute()
        )

        if not response.data:
            return print(status_code=404, content={"error": "User not found"})
        
        return {"user": response.data}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return print(status_code=500, content={"error": str(e)})
    


