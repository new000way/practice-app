import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 페이지 설정
st.set_page_config(page_title="게임 유저 데이터 분석", layout="wide")

# 제목
st.title("🎮 게임 유저 시각화 대시보드 (Demo)")

# 더미 데이터 생성
np.random.seed(42)
num_users = 1000

data = {
    "UserID": np.arange(1, num_users + 1),
    "GameGenre": np.random.choice(["Action", "RPG", "Strategy", "Puzzle", "Sports"], num_users),
    "PlayTime": np.random.exponential(scale=2, size=num_users).round(2),
    "Age": np.random.randint(13, 50, num_users),
    "Country": np.random.choice(["Korea", "USA", "Japan", "Germany", "Brazil"], num_users),
    "InGamePurchase": np.random.choice(["Yes", "No"], num_users, p=[0.3, 0.7]),
}

df = pd.DataFrame(data)

# --- 사이드바 필터 --- #
st.sidebar.header("🔍 필터 옵션")

selected_genre = st.sidebar.multiselect(
    "게임 장르 선택",
    options=df["GameGenre"].unique(),
    default=df["GameGenre"].unique()
)

selected_country = st.sidebar.multiselect(
    "국가 선택",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)

playtime_range = st.sidebar.slider(
    "플레이타임 범위 선택 (시간)",
    min_value=float(df["PlayTime"].min()),
    max_value=float(df["PlayTime"].max()),
    value=(float(df["PlayTime"].min()), float(df["PlayTime"].max()))
)

# 필터 적용
filtered_df = df[
    (df["GameGenre"].isin(selected_genre)) &
    (df["Country"].isin(selected_country)) &
    (df["PlayTime"].between(playtime_range[0], playtime_range[1]))
]

# --- 본문 콘텐츠 --- #
st.header("📊 필터링된 데이터 미리보기")
st.dataframe(filtered_df.head())

col1, col2 = st.columns(2)

# 1. 장르 분포
with col1:
    st.subheader("🎮 선택된 장르 분포")
    genre_counts = filtered_df["GameGenre"].value_counts()
    st.bar_chart(genre_counts)

# 2. 나라별 평균 플레이타임
with col2:
    st.subheader("🌍 국가별 평균 플레이타임")
    avg_playtime_by_country = filtered_df.groupby("Country")["PlayTime"].mean()
    st.bar_chart(avg_playtime_by_country)

st.header("👥 나이별 평균 플레이타임")
age_playtime = filtered_df.groupby("Age")["PlayTime"].mean()
st.line_chart(age_playtime)

st.header("💸 인게임 구매 여부에 따른 평균 플레이타임")
purchase_playtime = filtered_df.groupby("InGamePurchase")["PlayTime"].mean()
st.bar_chart(purchase_playtime)

st.caption("Demo Dashboard by YOU - Powered by Streamlit 🚀")
