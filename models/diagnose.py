from pydantic import BaseModel
from typing import Optional
from models.users import JobType, DrinkingType, SmokingType, DriverLicenseType

class DiagnoseRequest(BaseModel):
    user_id: int
    job: Optional[JobType] = None
    drinking: Optional[DrinkingType] = None
    smoking: Optional[SmokingType] = None
    drive_license: Optional[DriverLicenseType] = None