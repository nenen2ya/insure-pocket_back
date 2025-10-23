from fastapi import APIRouter

from db import supabase

router = APIRouter(prefix="/products")

@router.get("/{user_id}")
def get_user_products(user_id: int):
    # user_products 기준으로, 연결된 products 및 companies 가져오기
    try:
        response = supabase.table("user_products").select("""
            id,
            product_id,
            products(
                id,
                product_name,
                companies(company_name)
            )
        """).eq("user_id", user_id).execute()

    except Exception as e:
        print("Supabase API 오류:", e)
        return {"error": str(e)}

    # 데이터 정리
    user_products = response.data
    result = [
        {
            "product_id": up["products"]["id"],
            "product_name": up["products"]["product_name"],
            "company_name": (
                up["products"]["companies"]["company_name"]
                if up["products"].get("companies")
                else None
            ),
        }
        for up in user_products
        if up.get("products")
    ]

    return {"user_id": user_id, "products": result}