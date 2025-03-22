import streamlit as st
from sentence_transformers import SentenceTransformer, util
import torch
import os
import random

# 충돌 방지
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"

# 모델 로딩
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 음료 DB
drink_data = [
    {
        "name": "아이스 아메리카노",
        "desc": "시원하고 깔끔한 맛의 아이스 커피",
        "ingredients": ["커피", "물", "얼음"],
        "image": "https://cdn.pixabay.com/photo/2020/05/03/14/20/iced-coffee-5127280_960_720.jpg",
        "recipe": "에스프레소 2샷 + 차가운 물 + 얼음을 넣어주세요."
    },
    {
        "name": "핫초코",
        "desc": "달콤하고 부드러운 따뜻한 음료",
        "ingredients": ["우유", "초콜릿", "설탕"],
        "image": "https://cdn.pixabay.com/photo/2016/11/29/05/07/hot-chocolate-1869658_960_720.jpg",
        "recipe": "우유를 데우고, 초콜릿과 설탕을 넣고 잘 저어주세요."
    },
    {
        "name": "에너지 드링크",
        "desc": "카페인 가득한 에너지 부스터",
        "ingredients": ["카페인", "당", "타우린"],
        "image": "https://cdn.pixabay.com/photo/2017/03/27/13/53/energy-drink-2179032_960_720.jpg",
        "recipe": "캔을 따서 마시면 완성입니다 😉"
    },
    {
        "name": "레모네이드",
        "desc": "상큼하고 상쾌한 탄산 레모네이드",
        "ingredients": ["레몬", "탄산수", "설탕"],
        "image": "https://cdn.pixabay.com/photo/2017/05/23/22/36/lemonade-2333426_960_720.jpg",
        "recipe": "레몬즙 + 설탕 + 탄산수 섞고 얼음 넣으면 끝!"
    },
    {
        "name": "말차 라떼",
        "desc": "부드럽고 진한 녹차 라떼",
        "ingredients": ["말차", "우유", "설탕"],
        "image": "https://cdn.pixabay.com/photo/2020/09/30/17/44/matcha-5616305_960_720.jpg",
        "recipe": "말차 가루를 뜨거운 물에 풀고 우유와 섞어주세요."
    }
]

# 세션 상태 초기화
if "history" not in st.session_state:
    st.session_state.history = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

st.title("☕ AI 음료 추천 서비스")
st.markdown("기분, 상황, 재료를 기반으로 나만의 음료를 찾아보세요!")

# 사용자 입력
user_input = st.text_input("💬 지금 기분이나 상황은 어떤가요?")

# 재료 필터
all_ingredients = sorted(set(ing for drink in drink_data for ing in drink["ingredients"]))
excluded = st.multiselect("❌ 제외하고 싶은 재료", all_ingredients)

# ✨ 추천 버튼 (로딩 애니메이션 포함)
if st.button("✨ 추천 받기"):
    if not user_input.strip():
        st.warning("기분이나 상황을 입력해주세요!")
    else:
        with st.spinner("AI가 당신에게 어울리는 음료를 고르고 있어요... 🍹"):
            filtered_drinks = [
                drink for drink in drink_data
                if not any(ingredient in excluded for ingredient in drink["ingredients"])
            ]

            if not filtered_drinks:
                st.warning("선택한 재료를 제외하면 추천 가능한 음료가 없습니다.")
            else:
                emb_user = model.encode(user_input, convert_to_tensor=True)
                emb_drinks = model.encode([d["desc"] for d in filtered_drinks], convert_to_tensor=True)

                scores = util.cos_sim(emb_user, emb_drinks)[0]
                top_k = torch.topk(scores, k=min(3, len(filtered_drinks)))

                st.subheader("🔍 AI 추천 Top 3")

                for i, idx in enumerate(top_k.indices):
                    drink = filtered_drinks[idx]
                    score = top_k.values[i].item()

                    st.markdown(f"### {i+1}. **{drink['name']}**")
                    st.image(drink["image"], width=250)
                    st.markdown(f"📝 {drink['desc']}")
                    st.markdown(f"📌 추천 이유: 입력 내용과의 유사도 `{score:.2f}`")
                    st.markdown(f"📖 레시피: {drink['recipe']}")

                    if st.button(f"❤️ '{drink['name']}' 찜하기", key=f"fav_{i}"):
                        st.session_state.favorites.append(drink["name"])

                    st.markdown("---")

                st.session_state.history.append({
                    "input": user_input,
                    "top_choice": filtered_drinks[top_k.indices[0]]["name"]
                })

# 🎲 랜덤 추천 기능
if st.button("🎲 오늘의 랜덤 음료 추천!"):
    drink = random.choice(drink_data)
    st.subheader(f"🍹 랜덤 추천: {drink['name']}")
    st.image(drink["image"], width=250)
    st.markdown(f"📝 {drink['desc']}")
    st.markdown(f"📖 레시피: {drink['recipe']}")

    if st.button(f"❤️ '{drink['name']}' 찜하기"):
        st.session_state.favorites.append(drink["name"])
    st.stop()

# 🕘 히스토리
if st.session_state.history:
    st.subheader("🕘 내 추천 히스토리")
    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"💬 '{item['input']}' → **{item['top_choice']}**")

# ❤️ 찜 목록
if st.session_state.favorites:
    st.subheader("❤️ 내가 찜한 음료")
    st.markdown(", ".join(set(st.session_state.favorites)))