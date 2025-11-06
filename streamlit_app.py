import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 페이지 제목
st.title("게임 유저 데이터 시각화 대시보드 (데모)")

# 데이터 생성
np.random.seed(42)
num_users = 1000

data = {
    "UserID": np.arange(1, num_users + 1),
    "GameGenre": np.random.choice(["Action", "RPG", "Strategy", "Puzzle", "Sports"], num_users),
    "PlayTime": np.random.exponential(scale=2, size=num_users).round(2),
    "Age": np.random.randint(13, 50, num_users),
    "Country": np.random.choice(["Korea", "USA", "Japan", "Germany", "Brazil"], num_users)
}

df = pd.DataFrame(data)

# 기본 통계
st.header("📊 기본 통계 요약")
st.dataframe(df.describe())

# 장르 분포
st.header("🎮 게임 장르 분포")
genre_counts = df["GameGenre"].value_counts()
st.bar_chart(genre_counts)

# 플레이타임 통계
st.header("⏱️ 플레이타임 분포")
fig, ax = plt.subplots()
sns.histplot(df["PlayTime"], kde=True, ax=ax)
st.pyplot(fig)

# 나이별 플레이타임
st.header("👥 나이에 따른 평균 플레이타임")
age_playtime = df.groupby("Age")["PlayTime"].mean()
st.line_chart(age_playtime)
