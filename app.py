import streamlit as st
from sentence_transformers import SentenceTransformer, util
import torch
import os
import random

# 충돌 방지용 환경변수
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"

# 모델 로드
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 음료 데이터 (3개국어)
drink_data = [
    {
        "name": {
            "한국어": "아이스 아메리카노",
            "English": "Iced Americano",
            "Indonesia": "Americano Dingin"
        },
        "desc": {
            "한국어": "시원하고 깔끔한 맛의 아이스 커피",
            "English": "Chilled, clean-flavored iced coffee",
            "Indonesia": "Kopi dingin dengan rasa segar dan bersih"
        },
        "ingredients": {
            "한국어": ["커피", "물", "얼음"],
            "English": ["coffee", "water", "ice"],
            "Indonesia": ["kopi", "air", "es batu"]
        },
        "image": "https://cdn.pixabay.com/photo/2020/05/03/14/20/iced-coffee-5127280_960_720.jpg",
        "recipe": {
            "한국어": "에스프레소 2샷 + 물 + 얼음",
            "English": "2 shots of espresso + water + ice",
            "Indonesia": "2 shot espresso + air + es batu"
        }
    },
    {
        "name": {
            "한국어": "핫초코",
            "English": "Hot Chocolate",
            "Indonesia": "Cokelat Panas"
        },
        "desc": {
            "한국어": "달콤하고 부드러운 따뜻한 음료",
            "English": "Sweet and creamy warm drink",
            "Indonesia": "Minuman hangat yang manis dan lembut"
        },
        "ingredients": {
            "한국어": ["우유", "초콜릿", "설탕"],
            "English": ["milk", "chocolate", "sugar"],
            "Indonesia": ["susu", "cokelat", "gula"]
        },
        "image": "https://cdn.pixabay.com/photo/2016/11/29/05/07/hot-chocolate-1869658_960_720.jpg",
        "recipe": {
            "한국어": "우유 + 초콜릿 + 설탕 데우기",
            "English": "Heat milk + chocolate + sugar",
            "Indonesia": "Panaskan susu + cokelat + gula"
        }
    },
    {
        "name": {
            "한국어": "에너지 드링크",
            "English": "Energy Drink",
            "Indonesia": "Minuman Energi"
        },
        "desc": {
            "한국어": "카페인 가득한 에너지 부스터",
            "English": "A caffeine-packed energy booster",
            "Indonesia": "Booster energi dengan banyak kafein"
        },
        "ingredients": {
            "한국어": ["카페인", "당", "타우린"],
            "English": ["caffeine", "sugar", "taurine"],
            "Indonesia": ["kafein", "gula", "taurin"]
        },
        "image": "https://cdn.pixabay.com/photo/2017/03/27/13/53/energy-drink-2179032_960_720.jpg",
        "recipe": {
            "한국어": "그냥 따서 마시면 끝!",
            "English": "Just open the can and enjoy!",
            "Indonesia": "Buka kaleng dan langsung diminum!"
        }
    }
]

# 다국어 UI 텍스트
TEXTS = {
    "한국어": {
        "title": "☕ AI 음료 추천 서비스",
        "subtitle": "기분, 상황, 재료를 기반으로 나만의 음료를 찾아보세요!",
        "input_label": "💬 지금 기분이나 상황은 어떤가요?",
        "filter_label": "❌ 제외하고 싶은 재료",
        "recommend_button": "✨ 추천 받기",
        "random_button": "🎲 오늘의 랜덤 음료 추천!",
        "loading": "AI가 당신에게 어울리는 음료를 고르고 있어요... 🍹",
        "reason": "📌 추천 이유: 입력 내용과의 유사도",
        "recipe": "📖 레시피",
        "history": "🕘 내 추천 히스토리",
        "favorites": "❤️ 내가 찜한 음료",
        "warning_input": "기분이나 상황을 입력해주세요!",
        "warning_no_result": "선택한 재료를 제외하면 추천 가능한 음료가 없습니다.",
        "random_result": "🍹 랜덤 추천"
    },
    "English": {
        "title": "☕ AI Drink Recommender",
        "subtitle": "Find your perfect drink based on mood, situation, and ingredients!",
        "input_label": "💬 What's your current mood or situation?",
        "filter_label": "❌ Ingredients you want to avoid",
        "recommend_button": "✨ Get Recommendation",
        "random_button": "🎲 Random Drink of the Day!",
        "loading": "AI is selecting the best drink for you... 🍹",
        "reason": "📌 Why recommended: Similarity with your input",
        "recipe": "📖 Recipe",
        "history": "🕘 Recommendation History",
        "favorites": "❤️ My Favorite Drinks",
        "warning_input": "Please enter your mood or situation!",
        "warning_no_result": "No drinks available with the selected filters.",
        "random_result": "🍹 Random Recommendation"
    },
    "Indonesia": {
        "title": "☕ Rekomendasi Minuman AI",
        "subtitle": "Temukan minuman sempurna berdasarkan suasana hati, situasi, dan bahan!",
        "input_label": "💬 Bagaimana suasana hati atau situasimu sekarang?",
        "filter_label": "❌ Bahan yang ingin kamu hindari",
        "recommend_button": "✨ Dapatkan Rekomendasi",
        "random_button": "🎲 Rekomendasi Acak Hari Ini!",
        "loading": "AI sedang memilih minuman terbaik untukmu... 🍹",
        "reason": "📌 Alasan direkomendasikan: Mirip dengan input kamu",
        "recipe": "📖 Resep",
        "history": "🕘 Riwayat Rekomendasi",
        "favorites": "❤️ Minuman Favoritku",
        "warning_input": "Silakan masukkan suasana hati atau situasimu!",
        "warning_no_result": "Tidak ada minuman yang cocok dengan filter yang dipilih.",
        "random_result": "🍹 Rekomendasi Acak"
    }
}

# 세션 초기화
if "history" not in st.session_state:
    st.session_state.history = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

# 언어 선택
language = st.radio("🌐 Language / 언어 선택", ["한국어", "English", "Indonesia"])
T = TEXTS[language]

st.title(T["title"])
st.markdown(T["subtitle"])

# 사용자 입력
user_input = st.text_input(T["input_label"])

# 다국어 재료 필터
all_ingredients = sorted(set(ing for drink in drink_data for ing in drink["ingredients"][language]))
excluded = st.multiselect(T["filter_label"], all_ingredients)

# 추천 버튼
if st.button(T["recommend_button"]):
    if not user_input.strip():
        st.warning(T["warning_input"])
    else:
        with st.spinner(T["loading"]):
            filtered = [
                d for d in drink_data
                if not any(x in excluded for x in d["ingredients"][language])
            ]
            if not filtered:
                st.warning(T["warning_no_result"])
            else:
                emb_user = model.encode(user_input, convert_to_tensor=True)
                emb_drinks = model.encode([d["desc"][language] for d in filtered], convert_to_tensor=True)
                scores = util.cos_sim(emb_user, emb_drinks)[0]
                top_k = torch.topk(scores, k=min(3, len(filtered)))

                for i, idx in enumerate(top_k.indices):
                    drink = filtered[idx]
                    score = top_k.values[i].item()
                    st.markdown(f"### {i+1}. {drink['name'][language]}")
                    st.image(drink["image"], width=250)
                    st.markdown(f"📝 {drink['desc'][language]}")
                    st.markdown(f"{T['reason']}: `{score:.2f}`")
                    st.markdown(f"{T['recipe']}: {drink['recipe'][language]}")
                    if st.button(f"❤️ {drink['name'][language]}", key=f"fav_{i}"):
                        st.session_state.favorites.append(drink["name"][language])
                    st.markdown("---")

                st.session_state.history.append({
                    "input": user_input,
                    "top_choice": filtered[top_k.indices[0]]["name"][language]
                })

# 히스토리
if st.session_state.history:
    st.subheader(T["history"])
    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"💬 '{item['input']}' → **{item['top_choice']}**")

# 찜 목록
if st.session_state.favorites:
    st.subheader(T["favorites"])
    st.markdown(", ".join(set(st.session_state.favorites)))

# 랜덤 추천
if st.button(T["random_button"]):
    drink = random.choice(drink_data)
    st.subheader(f"{T['random_result']}: {drink['name'][language]}")
    st.image(drink["image"], width=250)
    st.markdown(f"📝 {drink['desc'][language]}")
    st.markdown(f"{T['recipe']}: {drink['recipe'][language]}")
    if st.button(f"❤️ {drink['name'][language]}", key="rand_fav"):
        st.session_state.favorites.append(drink["name"][language])
    st.stop()