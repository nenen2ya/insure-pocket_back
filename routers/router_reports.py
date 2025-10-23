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
def detail_report(user_id: int, category: str):
    df = compare_user_coverage(user_id)

    # 🔹 카테고리별 보장금액 비교
    categories_compare = [
        {
            "category": idx,
            "recommend": row["권장보장금액(만원)"],
            "current": row["현재보장금액(만원)"]
        }
        for idx, row in df.iterrows()
    ]

    shortage = df[df["백분율"] < 0].sort_values(by="백분율")
    subcategory_names = shortage.index.tolist()

    recommend_products = []
    added_product_ids = set()

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

        coverage_resp = (
            supabase.table("coverage")
            .select("product_id")
            .eq("subcategory_id", subcat_id)
            .execute()
        )
        if not coverage_resp.data:
            continue

        for cov in coverage_resp.data:
            product_id = cov["product_id"]

            if product_id in added_product_ids:
                continue

            prod_resp = (
                supabase.table("products")
                .select("""
                    *,
                    companies(company_name, url)
                """)
                .eq("id", product_id)
                .execute()
            )
            if not prod_resp.data:
                continue
            product_info = prod_resp.data[0]

            subcats_resp = (
                supabase.table("coverage")
                .select("""
                    subcategories(name, categories(type))
                """)
                .eq("product_id", product_id)
                .execute()
            )
            subcategory_info = [
                {
                    "subcategory_name": s["subcategories"]["name"],
                    "category_type": s["subcategories"]["categories"]["type"]
                }
                for s in subcats_resp.data
                if s.get("subcategories")
            ]

            recommend_products.append({
                "product_info": product_info,
                "subcategory_info": subcategory_info
            })
            added_product_ids.add(product_id)

            if len(recommend_products) >= 3:
                break
        if len(recommend_products) >= 3:
            break

    # 6️⃣ 최종 결과
    result = {
        "user_id": user_id,
        "category": category,
        "categories_compare": categories_compare,
        "products_recommendation": recommend_products
    }

    return result
