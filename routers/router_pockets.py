from fastapi import APIRouter
from fastapi import HTTPException

from db import supabase

router = APIRouter(prefix="/pockets")

@router.get("/{user_id}")
def get_user_pockets(user_id: int):
    try:
        response = (
    supabase.table("pockets")
    .select("""
        id,
        products(
            id,
            product_name,
            monthly_premium,
            keyword1, summary1,
            keyword2, summary2,
            keyword3, summary3,
            companies(
                company_name,
                url
            ),
            coverage(
                coverage_amount,
                subcategories(
                    name,
                    categories(
                        type
                    )
                )
            )
        )
    """)
    .eq("user_id", user_id)
    .execute()
)
        return response.data
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
    
@router.post("/{user_id}/{product_id}")
def post_user_pockets(user_id: int, product_id: int):
    try:
        existing = (
            supabase.table("pockets")
            .select("id")
            .eq("user_id", user_id)
            .eq("product_id", product_id)
            .execute()
        )

        if existing.data:
            raise HTTPException(status_code=400, detail="이미 찜한 상품입니다.")
        response = (
            supabase.table("pockets")
            .insert({"user_id": int(user_id), "product_id": int(product_id)})
            .execute()
        )

        return {"message": "상품이 찜 목록에 추가되었습니다.", "data": response.data[0]}

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}/{product_id}")
def delete_user_pockets(user_id: int, product_id: int):
    try:
        existing = (
            supabase.table("pockets")
            .select("id")
            .eq("user_id", user_id)
            .eq("product_id", product_id)
            .execute()
        )
        if not existing.data:
            raise HTTPException(status_code=404, detail="존재하지 않는 찜 정보입니다.")

        response = (
            supabase.table("pockets")
            .delete()
            .eq("user_id", user_id)
            .eq("product_id", product_id)
            .execute()
        )
        return {"message": "삭제 완료", "deleted": response.data}

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))