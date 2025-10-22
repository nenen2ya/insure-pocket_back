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
        "lack": int(lack_amount),
        "plus": int(plus_amount),
        "stand": int(stand_amount)
    }

    return result

# @router.get("/{user_id}/{category}")
# def detail_report(user_id: int):
#     df = compare_user_coverage(user_id)
#     categories_compare = [
#         {
#             "category": idx,  
#             "recommand": row["권장보장금액(만원)"],
#             "current": row["현재보장금액(만원)"]
#         }
#         for idx, row in df.iterrows()
#     ]

#     recommend_prod = (
#         df[df["백분율"] < 0].sort_values(by="백분율").index.tolist()
#     )


#     products_recommendation = (
#         supabase.table("product")
#         .select(po)
#         .eq("id", request.user_id)
#         .execute()
#     )

#     result = {
#         "user_id": user_id,
#         "categories_compare": categories_compare,
#         "products_recommendation": products_recommendation
#     }

#     return result