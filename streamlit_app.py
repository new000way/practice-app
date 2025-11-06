import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# 페이지 레이아웃 설정
st.set_page_config(page_title="게임 유저 참여도 예측 대시보드", layout="wide")

st.title("🎮 게임 유저 참여 예측 대시보드")

# --- 사이드바 ---
st.sidebar.header("설정")

# 파일 업로드
data_file = st.sidebar.file_uploader("CSV 데이터 파일 업로드", type=['csv'])
if data_file:
    df = pd.read_csv(data_file)

    # 데이터 전처리: 타겟 및 피처 설정
    target = 'EngagementLevel'
    features = df.drop(columns=['PlayerID', target])

    # 레이블 인코딩 (문자형 데이터 대비)
    df = pd.get_dummies(df)

    # 탭 레이아웃
    tab1, tab2, tab3, tab4 = st.tabs(["📊 데이터 탐색", "📈 참여도 시각화", "🧠 모델 학습", "🔮 참여도 예측"])

    # --- 탭1: 데이터 탐색 ---
    with tab1:
        st.subheader("데이터 샘플")
        st.write(df.head())

        st.subheader("기본 통계 요약")
        st.write(df.describe())

        st.subheader("장르 분포")
        st.bar_chart(df['GameGenre'].value_counts())

    # --- 탭2: 참여도 시각화 ---
    with tab2:
        st.subheader("EngagementLevel 분포")
        st.bar_chart(df[target].value_counts())

        st.subheader("플레이 시간에 따른 참여도")
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x='EngagementLevel', y='PlayTimeHours')
        st.pyplot(fig)

    # --- 탭3: 모델 학습 ---
    with tab3:
        if st.button("모델 학습 시작"):
            X = df.drop(target, axis=1)
            y = df[target]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            st.subheader("모델 성능")
            st.text(classification_report(y_test, y_pred))

            st.subheader("혼동 행렬")
            fig, ax = plt.subplots()
            cm = confusion_matrix(y_test, y_pred)
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            st.pyplot(fig)

    # --- 탭4: 참여도 예측 도구 ---
    with tab4:
        st.subheader("유저 데이터 입력 → 참여도 예측")

        # 특정 속성 입력 받기
        age = st.slider("나이", 10, 70, 25)
        playtime = st.slider("총 플레이시간(시간)", 0.1, 1000.0, 50.0)
        purchases = st.number_input("인게임 구매 횟수", 0, 100, 0)
        sessions = st.slider("주간 평균 세션 수", 1, 40, 10)
        difficulty = st.selectbox("난이도 선호", ["Easy", "Medium", "Hard"])

        # 입력 배열 생성
        input_data = [[age, playtime, purchases, sessions, difficulty]]
        input_df = pd.DataFrame(input_data, columns=['Age', 'PlayTimeHours', 'InGamePurchases', 'SessionsPerWeek', 'GameDifficulty'])
        input_df = pd.get_dummies(input_df).reindex(columns=X.columns, fill_value=0)

        if st.button("참여도 예측하기"):
            prediction = model.predict(input_df)[0]
            st.success(f"예상 참여도 수준: {prediction}")
