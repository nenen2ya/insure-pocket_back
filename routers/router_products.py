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


@router.get("/recommendations/{user_id}")
def get_recommended_products(user_id: int):
    # 간단한 추천 로직: 사용자가 없는 제품 중에서 상위 5개 제품 추천
    user_products_response = supabase.table("user_products").select("product_id").eq("user_id", user_id).execute()
    
    # if user_products_response.error:
    #     return {"error": user_products_response.error.message}

    owned_product_ids = [up["product_id"] for up in user_products_response.data]

    recommended_response = supabase.table("products").select("""
        id,
        product_name,
        companies(company_name)
    """).not_("id", "in", f"({','.join(map(str, owned_product_ids))})").limit(5).execute()

    # if recommended_response.error:
    #     return {"error": recommended_response.error.message}

    recommendations = [
        {
            "product_id": prod["id"],
            "product_name": prod["product_name"],
            "company_name": (
                prod["companies"]["company_name"]
                if prod.get("companies")
                else None
            ),
        }
        for prod in recommended_response.data
    ]

    return {"user_id": user_id, "recommended_products": recommendations}