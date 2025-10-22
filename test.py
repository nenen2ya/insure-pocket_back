# 
# =============================================
#  INSURE POCKET : 개인화 권장 보장금액 계산기
# =============================================
# 기능 요약:
# - Supabase의 users 테이블에서 사용자 정보 불러옴
# - 위험도 데이터(risk_df) 기반으로 종합위험비 계산
# - 평균 치료비와 곱해서 권장 보장금액 산출
# - 결과를 pandas DataFrame으로 출력
# =============================================

from db import supabase
import pandas as pd

# -------------------------------------------------------
# 1️⃣ 위험비 데이터 정의
# -------------------------------------------------------
cancers = ["간암", "췌장암", "폐암", "위암", "대장암", "유방암", "갑상선암"]

data = {
    "연령": {
        "0-14": [0.007, 0.008, 0.005, 0.009, 0.008, 0.007, 0.006],
        "15-34": [0.048, 0.052, 0.036, 0.060, 0.052, 0.047, 0.042],
        "35-64": [0.272, 0.297, 0.203, 0.338, 0.297, 0.264, 0.235],
        "65이상": [0.785, 0.855, 0.584, 0.974, 0.855, 0.762, 0.678],
    },
    "성별": {
        "여": [0.088, 0.087, 0.068, 0.139, 0.074, 0.537, 0.597],
        "남": [0.246, 0.095, 0.138, 0.275, 0.108, 0.003, 0.203],
    },
    "흡연": {
        "비흡연자": [0.057, 0.103, 0.117, 0.070, 0.062, 0.028, 0.014],
        "하루 10개비 이하": [0.193, 0.349, 0.398, 0.239, 0.210, 0.093, 0.046],
        "하루 10개비 초과": [0.252, 0.457, 0.520, 0.312, 0.274, 0.122, 0.060],
    },
    "음주": {
        "주 0병": [0.218, 0.153, 0.100, 0.093, 0.254, 0.180, 0.034],
        "주 1-3병": [0.262, 0.154, 0.102, 0.100, 0.257, 0.236, 0.034],
        "주 4병 이상": [0.354, 0.239, 0.106, 0.115, 0.398, 0.394, 0.053],
    },
    "직업군": {
        "저위험군": [0.059, 0.065, 0.147, 0.073, 0.065, 0.058, 0.171],
        "고위험군": [0.107, 0.117, 0.267, 0.133, 0.117, 0.104, 0.309],
    },
    "운전": {
        "비운전자": [0.028, 0.030, 0.034, 0.034, 0.030, 0.027, 0.040],
        "운전자": [0.028, 0.030, 0.034, 0.034, 0.030, 0.027, 0.040],
    }
}

risk_df = {k: pd.DataFrame(v, index=cancers).T for k, v in data.items()}

# 평균 치료비 (단위: 만원)
treatment_costs = {
    "간암": 6623,
    "췌장암": 6372,
    "폐암": 4657,
    "위암": 2686,
    "대장암": 2352,
    "유방암": 1769,
    "갑상선암": 1126
}

# -------------------------------------------------------
# 2️⃣ Supabase에서 user 데이터 가져오기
# -------------------------------------------------------
def get_user_data(user_id: int):
    response = supabase.table("users").select(
        "age, gender, job, drinking, smoking, drive_license"
    ).eq("id", user_id).execute()

    if not response.data:
        raise ValueError(f"❌ User ID {user_id} not found")

    return response.data[0]


# -------------------------------------------------------
# 3️⃣ enum → 위험표 key로 매핑
# -------------------------------------------------------
mapping = {
    "gender": {"Male": "남", "Female": "여"},
    "job": {"low": "저위험군", "high": "고위험군"},
    "drinking": {
        "none": "주 0병",
        "weekly_3": "주 1-3병",
        "weekly_4_plus": "주 4병 이상",
    },
    "smoking": {
        "none": "비흡연자",
        "less_than_10": "하루 10개비 이하",
        "more_than_10": "하루 10개비 초과",
    },
    "drive_license": {"YES": "운전자", "NO": "비운전자"},
}


# -------------------------------------------------------
# 4️⃣ 위험비 계산 함수
# -------------------------------------------------------
def calculate_recommendation(user_id: int):
    user_data = get_user_data(user_id)

    # 나이대 분류
    age = user_data["age"]
    if age < 15:
        age_group = "0-14"
    elif age < 35:
        age_group = "15-34"
    elif age < 65:
        age_group = "35-64"
    else:
        age_group = "65이상"

    # 사용자 선택값 매핑
    user_choice = {
        "연령": age_group,
        "성별": mapping["gender"][user_data["gender"]],
        "흡연": mapping["smoking"][user_data["smoking"]],
        "음주": mapping["drinking"][user_data["drinking"]],
        "직업군": mapping["job"][user_data["job"]],
        "운전": mapping["drive_license"][user_data["drive_license"]],
    }

    # 종합위험비 계산
    total_risk = pd.Series(0, index=cancers)
    for category, choice in user_choice.items():
        total_risk += risk_df[category].loc[choice]

    # 권장 보장금액 계산
    recommend_amount = total_risk * pd.Series(treatment_costs)

    # 결과 DataFrame 구성
    result_df = pd.DataFrame({
        "종합위험비": total_risk.round(3),
        "평균치료비(만원)": pd.Series(treatment_costs),
        "권장보장금액(만원)": recommend_amount.round(1)
    })

    return user_choice, result_df


# -------------------------------------------------------
# 5️⃣ 실행 (테스트)
# -------------------------------------------------------
if __name__ == "__main__":
    user_id = 6  # 예시
    user_choice, result_df = calculate_recommendation(user_id)

    print("✅ 사용자 정보:")
    print(user_choice)
    print("\n🧮 [종합위험비 및 권장보장금액]")
    print(result_df)
