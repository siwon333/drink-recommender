# 🥤 Drink Recommender

AI 기반 음료 추천 웹앱입니다. 기분이나 상황을 입력하면, 적절한 음료를 추천해줍니다. 
한국어 / 영어 / 인도네시아어를 지원하며, 유사도 기반 추천과 랜덤 추천 기능이 있습니다.

🚀 **바로 보기**: [drink-recommender.streamlit.app](https://drink-recommender-eytmi5bgwcvtsmunsnyt6a.streamlit.app/)

---

## 📌 주요 기능

- 💬 **기분/상황 입력** → AI가 음료 추천
- 🢨 **재료 필터링** → 제제하고 싶은 재료 선택
- 🏆 **Top 3 유사도 추천** → 가장 잘 맞는 3가지 음료 표시
- 🎲 **랜덤 추천** → 오늘의 랜덤 음료!
- 🥘 **히스토리** → 이전 추천 내역 확인
- 🌐 **다국어 지원** → 한국어 / 영어 / 인도네시아어

---

## 🖼️ 스크린샷

![image](https://github.com/user-attachments/assets/c48adc29-8489-4196-894d-12d3b3ab0aa7)

---

## ⚙️ 설치 및 실행 방법

1. 이 저장소를 클론합니다.
```bash
git clone https://github.com/siwon333/drink-recommender.git
cd drink-recommender
```

2. 가상환경 생성 (선택)
```bash
python -m venv venv
source venv/bin/activate  # 또는 Windows: venv\Scripts\activate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. 앱 실행
```bash
streamlit run app.py
```

---

## 📁 프로젝트 구성

```
drink-recommender/
├── app.py                  # 메인 Streamlit 앱
├── drinks_data.json        # 음료 데이터 (다국어 포함)
├── requirements.txt        # 의존성 목록
├── img/                    # 음료 이미지 폴더
│   ├── AA.jpg
│   ├── BS.jpg
│   └── ...
```

---

## ☁️ 배포하기 (Streamlit Cloud)

1. [Streamlit Cloud](https://streamlit.io/cloud)에 접속
2. GitHub 계정 연결 → 해당 저장소 선택
3. 메인 파일로 `app.py` 선택
4. Deploy 버튼 클릭!

---

## 🙌 크레리트

- 개발자: [siwon333](https://github.com/siwon333)
- AI 모델: SentenceTransformer (`paraphrase-MiniLM-L6-v2`)
- 이미지 출처: [Pixabay](https://pixabay.com/)

---

## 📬 문의

궁금한 점이나 제안이 있다면 이슈로 남겨주세요! 감사합니다 ☕

