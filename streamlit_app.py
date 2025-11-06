import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

st.set_page_config(page_title="게임 유저 참여 예측 대시보드", layout="wide")

st.title("🎮 게임 유저 참여도 예측 대시보드")

# --- 사이드바 ---
st.sidebar.header("설정")

# 파일 업로드
data_file = st.sidebar.file_uploader("CSV 데이터 파일 업로드", type=['csv'])

if data_file:
    df = pd.read_csv(data_file)

    # --- 데이터 탐색 ---
    st.subheader("데이터 미리보기")
    st.write(df.head())

    # --- 장르 분포 시각화 (에러 방지 버전) ---
    st.subheader("🌀 게임 장르 분포")
    try:
        genre_counts = df['GameGenre'].value_counts()
        st.bar_chart(genre_counts)
    except Exception as e:
        st.error(f"장르 분포 시각화 중 오류 발생: {e}")

    # --- 참여도 분포 시각화 ---
    st.subheader("📊 참여도(Engagement Level) 분포")
    try:
        engagement_counts = df['EngagementLevel'].value_counts()
        st.bar_chart(engagement_counts)
    except Exception as e:
        st.error(f"참여도 시각화 중 오류 발생: {e}")

    # --- 플레이 시간 vs 참여도 상자그래프 ---
    st.subheader("⏱ 플레이 시간에 따른 참여도")
    try:
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x='EngagementLevel', y='PlayTimeHours')
        ax.set_title("PlayTimeHours by EngagementLevel")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"박스플롯 시각화 중 오류 발생: {e}")

    # --- 머신러닝 모델 학습 및 예측 ---
    st.subheader("🧠 머신러닝 모델 참여도 예측")
    try:
        # 데이터 전처리 (문자형 변환 → 원-핫)
        processed_df = pd.get_dummies(df, drop_first=True)

        # 타겟과 피처 분리
        X = processed_df.drop(columns=['EngagementLevel_Low', 'EngagementLevel_Medium', 'EngagementLevel_High'], errors='ignore')
        y = df['EngagementLevel']

        # Train/Test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        st.write("🔍 모델 평가 결과")
        st.text(classification_report(y_test, y_pred))

        # 혼동 행렬
        fig_cm, ax_cm = plt.subplots()
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax_cm)
        ax_cm.set_title("Confusion Matrix")
        st.pyplot(fig_cm)

    except Exception as e:
        st.error(f"모델 학습/예측 중 오류 발생: {e}")

else:
    st.info("좌측 사이드바에서 CSV 파일을 업로드해주세요.")
