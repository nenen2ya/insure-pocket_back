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

@router.get("/{user_id}/{category}")
def detail_report(user_id: int):
    df = compare_user_coverage(user_id)

    categories_compare = [
        {
            "category": idx,
            "recommand": row["권장보장금액(만원)"],
            "current": row["현재보장금액(만원)"]
        }
        for idx, row in df.iterrows()
    ]

    shortage = df[df["백분율"] < 0].sort_values(by="백분율")
    subcategory_names = shortage.index.tolist()

    recommend_products = []
    added_product_ids = set()
    cond = True
 
    while cond:
        for name in subcategory_names:
            subcat_resp = (
                supabase.table("subcategories")
                .select("id")
                .eq("name", name)
                .execute()
            )
            if not subcat_resp.data:
                continue
            subcat_id = subcat_resp.data[0]["id"]

            response = (
                supabase.table("coverage")
                .select("""
                    product_id,
                    subcategories(name, categories(type))
                """)
                .eq("subcategory_id", subcat_id)
                .execute()
            )

            for item in response.data:
                if len(recommend_products) >= 3:
                    cond = False
                    break
                prod_id = item["product_id"]
                if prod_id not in added_product_ids:
                    recommend_products.append({
                        "subcategory": name,
                        "product_id": prod_id
                    })
                    added_product_ids.add(prod_id)



    result = {
        "user_id": user_id,
        "categories_compare": categories_compare,
        "products_recommendation": recommend_products
    }
    return result
