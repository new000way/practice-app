import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 페이지 설정
st.set_page_config(page_title="랜덤 게임 플레이 패턴 시뮬레이터", layout="wide")

# 제목
st.title("🎮 랜덤 게임 플레이 패턴 시뮬레이터 대시보드")

# 데이터 시뮬레이션
np.random.seed(42)
num_users = 3000

data = {
    "UserID": np.arange(1, num_users + 1),
    "GameGenre": np.random.choice(["Action", "RPG", "Strategy", "Puzzle", "Sports"], num_users),
    "PlayTime": np.random.gamma(shape=2, scale=2, size=num_users).round(2),
    "SessionCount": np.random.poisson(lam=3, size=num_users),
    "AvgSessionTime": np.random.uniform(0.5, 2.5, size=num_users).round(2),
    "Spend": np.random.exponential(scale=5000, size=num_users).round(2),
    "FavoriteHour": np.random.choice(np.arange(0, 24), num_users),
    "Country": np.random.choice(["Korea", "USA", "Japan", "Germany", "Brazil"], num_users)
}

df = pd.DataFrame(data)

# --- 사이드바 --- #
st.sidebar.header("🔍 필터 옵션")

selected_genres = st.sidebar.multiselect(
    "게임 장르 선택", df["GameGenre"].unique(), default=df["GameGenre"].unique()
)

max_spend = st.sidebar.slider("최대 구매 금액 (₩)", 0, int(df["Spend"].max()), (0, int(df["Spend"].max())))

playtime_range = st.sidebar.slider(
    "플레이타임 범위 (시간)", float(df["PlayTime"].min()), float(df["PlayTime"].max()), 
    (float(df["PlayTime"].min()), float(df["PlayTime"].max()))
)

filtered_df = df[
    (df["GameGenre"].isin(selected_genres)) &
    (df["Spend"].between(max_spend[0], max_spend[1])) &
    (df["PlayTime"].between(playtime_range[0], playtime_range[1]))
]

# --- 데이터 요약 --- #
st.header("📊 필터링된 데이터 미리보기")
st.dataframe(filtered_df.head())

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🕹️ 장르 분포")
    st.bar_chart(filtered_df["GameGenre"].value_counts())

with col2:
    st.subheader("💸 평균 지출 금액 (₩)")
    st.metric(label="평균 지출", value=f"{filtered_df['Spend'].mean():,.0f} ₩")

with col3:
    st.subheader("⏱️ 평균 플레이타임 (시간)")
    st.metric(label="평균 플레이타임", value=f"{filtered_df['PlayTime'].mean():.2f}시간")

st.header("⌚ 접속 시간대 분포 (가장 많은 시간)")
favorite_hours = filtered_df["FavoriteHour"].value_counts().sort_index()
st.bar_chart(favorite_hours)

st.header("🧠 세션당 평균 시간 vs 전체 플레이타임")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x="AvgSessionTime", y="PlayTime", hue="GameGenre", ax=ax)
plt.xlabel("AvgSessionTime")
plt.ylabel("PlayTime")
st.pyplot(fig)

st.caption("Simulation Dashboard by YOU - Powered by Streamlit 🚀")
