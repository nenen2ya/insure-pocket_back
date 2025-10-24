from fastapi import FastAPI
from db import supabase  # ← db.py에서 가져옴

from routers import router_diagnose
from routers import router_pockets
from routers import router_products
from routers import router_reports
from routers import router_users
from routers import router_auth

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 나중엔 localhost:3000 만 남기면 됨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_diagnose.router)
app.include_router(router_pockets.router)
app.include_router(router_products.router)
app.include_router(router_reports.router)
app.include_router(router_users.router)
app.include_router(router_auth.router)

@app.get("/")
def root():
    return {"message": "Supabase API 연결 성공"}


