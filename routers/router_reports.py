from fastapi import APIRouter
from db import supabase
from test import compare_user_coverage

router = APIRouter(prefix="/reports")

@router.get("/{user_id}")
def total_report(user_id: int):
    user_products_resp = (
            supabase
            .table("user_products")
            .select("""
                product_id,
                products (
                    product_name,
                    monthly_premium,
                    companies (company_name)
                )
            """)
            .eq("user_id", user_id)
            .execute()
        )
    user_products = user_products_resp.data if user_products_resp.data else []

    user_monthly_premium = (
            supabase
            .table("user_products")
            .select("products(monthly_premium)")
            .eq("user_id", user_id)
            .execute()
        )
    data = user_monthly_premium.data or []
    total_premium = sum(
        item["products"]["monthly_premium"]
        for item in data
        if item.get("products") and item["products"].get("monthly_premium")
    )

    df = compare_user_coverage(user_id)
    lack_amount = (df["보장상태"] == '부족').sum()
    plus_amount = (df["보장상태"] == '여유').sum()
    stand_amount = (df["보장상태"] == '적정').sum()

    result = {
        "user_id": user_id,
        "products": user_products,
        "total_monthly_premium": total_premium,
        "lack": lack_amount,
        "plus": plus_amount,
        "stand": stand_amount
    }

    return result

# @router.get("/{user_id}/{category}")
# def detail_report():