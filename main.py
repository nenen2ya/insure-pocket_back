from fastapi import FastAPI
from db import supabase  # ← db.py에서 가져옴

from routers import router_diagnose
from routers import router_pockets
from routers import router_products
from routers import router_reports
from routers import router_users

app = FastAPI()

app.include_router(router_diagnose.router)
app.include_router(router_pockets.router)
app.include_router(router_products.router)
app.include_router(router_reports.router)
app.include_router(router_users.router)

@app.get("/")
def root():
    return {"message": "Supabase API 연결 성공"}


