from fastapi import APIRouter
from models.diagnose import DiagnoseRequest
from db import supabase

router = APIRouter(prefix="/diagnose")

@router.post("/")
def user_diagnose(request: DiagnoseRequest):
    data = {
        "job": request.job.value,
        "drinking": request.drinking.value,
        "smoking": request.smoking.value,
        "drive_license": request.drive_license.value,
    }
    response = (
        supabase.table("users")
        .update(data)
        .eq("id", request.user_id)
        .execute()
    )

