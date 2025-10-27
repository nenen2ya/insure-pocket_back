from fastapi import APIRouter
from db import supabase

router = APIRouter(prefix="/products")

@router.get("/{user_id}")
def get_user_products(user_id: int):
    try:
        response = supabase.table("user_products").select("""
            id,
            product_id,
            users(
                user_name
            ),                                                          
            products(
                id,
                product_name,
                monthly_premium,
                company_id,
                companies(
                    id,
                    company_name
                )
            )
        """).eq("user_id", user_id).execute()

    except Exception as e:
        print("Supabase API 오류:", e)
        return {"error": str(e)}

    user_products = response.data or []
    user_name = None
    if user_products and user_products[0].get("users"):
        user_name = user_products[0]["users"]["user_name"]

    result = []
    for up in response.data:
        product = up.get("products")
        if not product:
            continue

        company = product.get("companies", {})

        result.append({
            "id": up["id"],
            "company_id": company.get("id"),
            "company_name": company.get("company_name"),
            "product_name": product.get("product_name"),
            "monthly_premium": product.get("monthly_premium"),
        })

    return {
        "user_id": user_id,
        "user_name": user_name,
        "user_products": result
    }
