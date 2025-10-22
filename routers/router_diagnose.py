from fastapi import APIRouter
from models.pockets import Pocket, PocketCreate

from db import supabase

router = APIRouter(prefix="/diagnose")