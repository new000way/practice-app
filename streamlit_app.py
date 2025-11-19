import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(page_title="🎮 게임 판매 대쉬보드", layout="wide", initial_sidebar_state="expanded")

# 제목 및 설명
st.title("🎮 게임 판매 데이터 분석 대쉬보드")
st.markdown("---")
st.markdown("**Kaggle Video Game Sales Dataset (2016년 기준)**")

# 데이터 로드 (캐싱)
@st.cache_data
def load_data():
    # Kaggle에서 다운로드한 CSV 파일 경로
    df = pd.read_csv('Video_Games_Sales_as_at_22_Dec_2016.csv')

    # 결측치 처리
    df = df.dropna(subset=['Year_of_Release', 'Critic_Score'])
    df['Year_of_Release'] = df['Year_of_Release'].astype(int)

    return df

df = load_data()

# ============================================
# 사이드바 필터 구성
# ============================================
st.sidebar.header("🔧 필터 옵션")

# 연도 범위 선택
year_range = st.sidebar.slider(
    "📅 연도 범위 선택",
    min_value=int(df['Year_of_Release'].min()),
    max_value=int(df['Year_of_Release'].max()),
    value=(2000, 2016),
    step=1
)

# 장르 선택
selected_genres = st.sidebar.multiselect(
    "🎯 장르 선택 (복수 선택 가능)",
    options=sorted(df['Genre'].unique()),
    default=sorted(df['Genre'].unique())
)

# 플랫폼 선택
selected_platforms = st.sidebar.multiselect(
    "🖥️ 플랫폼 선택",
    options=sorted(df['Platform'].unique()),
    default=sorted(df['Platform'].unique())[:5]  # 상위 5개만 기본 선택
)

# 필터 적용
filtered_df = df[
    (df['Year_of_Release'] >= year_range[0]) &
    (df['Year_of_Release'] <= year_range[1]) &
    (df['Genre'].isin(selected_genres)) &
    (df['Platform'].isin(selected_platforms))
]

# ============================================
# KPI 카드 (핵심 지표)
# ============================================
st.subheader("📊 핵심 지표 (KPI)")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_sales = filtered_df['Global_Sales'].sum()
    st.metric("총 판매량 (백만 단위)", f"{total_sales:.2f}M")

with col2:
    avg_rating = filtered_df['Critic_Score'].mean() / 10
    st.metric("평균 평점", f"{avg_rating:.1f} / 10")

with col3:
    game_count = len(filtered_df)
    st.metric("게임 수", f"{game_count:,}")

with col4:
    top_platform_sales = filtered_df.groupby('Platform')['Global_Sales'].sum().max()
    st.metric("플랫폼 최대 판매량", f"{top_platform_sales:.2f}M")

with col5:
    top_genre = filtered_df.groupby('Genre')['Global_Sales'].sum().idxmax()
    st.metric("최고 인기 장르", top_genre)

st.markdown("---")

# ============================================
# 탭 구성 (시각화)
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 지역별 판매", 
    "🎮 장르 분석", 
    "🖥️ 플랫폼 분석", 
    "⭐ 평점 분석",
    "🏆 순위"
])

# ============================================
# TAB 1: 지역별 판매
# ============================================
with tab1:
    st.subheader("지역별 판매량 비교")

    col1, col2 = st.columns(2)

    with col1:
        # 지역별 총 판매량
        regional_sales = {
            '북미': filtered_df['NA_Sales'].sum(),
            '유럽': filtered_df['EU_Sales'].sum(),
            '일본': filtered_df['JP_Sales'].sum(),
            '기타': filtered_df['Other_Sales'].sum()
        }

        fig_pie = px.pie(
            values=list(regional_sales.values()),
            names=list(regional_sales.keys()),
            title="📍 지역별 판매량 비율",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # 연도별 지역별 판매 트렌드
        yearly_regional = filtered_df.groupby('Year_of_Release').agg({
            'NA_Sales': 'sum',
            'EU_Sales': 'sum',
            'JP_Sales': 'sum',
            'Other_Sales': 'sum'
        }).reset_index()

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=yearly_regional['Year_of_Release'], 
                                     y=yearly_regional['NA_Sales'],
                                     mode='lines+markers', name='북미'))
        fig_line.add_trace(go.Scatter(x=yearly_regional['Year_of_Release'], 
                                     y=yearly_regional['EU_Sales'],
                                     mode='lines+markers', name='유럽'))
        fig_line.add_trace(go.Scatter(x=yearly_regional['Year_of_Release'], 
                                     y=yearly_regional['JP_Sales'],
                                     mode='lines+markers', name='일본'))

        fig_line.update_layout(title="📅 연도별 지역 판매 트렌드", 
                              xaxis_title="연도", 
                              yaxis_title="판매량 (백만 단위)",
                              hovermode='x unified')
        st.plotly_chart(fig_line, use_container_width=True)

# ============================================
# TAB 2: 장르 분석
# ============================================
with tab2:
    st.subheader("게임 장르 분석")

    col1, col2 = st.columns(2)

    with col1:
        # 장르별 판매량
        genre_sales = filtered_df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)

        fig_bar = px.bar(
            x=genre_sales.values,
            y=genre_sales.index,
            orientation='h',
            title="🎯 장르별 총 판매량",
            labels={'x': '판매량 (백만 단위)', 'y': '장르'}
        )
        fig_bar.update_traces(marker_color='steelblue')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # 장르별 게임 수
        genre_count = filtered_df['Genre'].value_counts()

        fig_bar2 = px.bar(
            x=genre_count.values,
            y=genre_count.index,
            orientation='h',
            title="📊 장르별 게임 수",
            labels={'x': '게임 수', 'y': '장르'}
        )
        fig_bar2.update_traces(marker_color='coral')
        st.plotly_chart(fig_bar2, use_container_width=True)

# ============================================
# TAB 3: 플랫폼 분석
# ============================================
with tab3:
    st.subheader("게임 플랫폼 분석")

    col1, col2 = st.columns(2)

    with col1:
        # 상위 10개 플랫폼 판매량
        platform_sales = filtered_df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10)

        fig_platform = px.bar(
            x=platform_sales.values,
            y=platform_sales.index,
            orientation='h',
            title="🏆 상위 10개 플랫폼 (판매량)",
            labels={'x': '판매량 (백만 단위)', 'y': '플랫폼'},
            color=platform_sales.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_platform, use_container_width=True)

    with col2:
        # 시간대별 플랫폼 변화
        platform_trend = filtered_df.groupby(['Year_of_Release', 'Platform'])['Global_Sales'].sum().reset_index()
        top_platforms = filtered_df.groupby('Platform')['Global_Sales'].sum().nlargest(5).index
        platform_trend_filtered = platform_trend[platform_trend['Platform'].isin(top_platforms)]

        fig_platform_trend = px.line(
            platform_trend_filtered,
            x='Year_of_Release',
            y='Global_Sales',
            color='Platform',
            title="📈 주요 플랫폼 판매 트렌드",
            labels={'Year_of_Release': '연도', 'Global_Sales': '판매량 (백만 단위)'}
        )
        st.plotly_chart(fig_platform_trend, use_container_width=True)

# ============================================
# TAB 4: 평점 분석
# ============================================
with tab4:
    st.subheader("게임 평점 분석")

    col1, col2 = st.columns(2)

    with col1:
        # 평점과 판매량의 상관관계
        fig_scatter = px.scatter(
            filtered_df,
            x='Critic_Score',
            y='Global_Sales',
            color='Genre',
            size='Global_Sales',
            hover_name='Name',
            title="⭐ 평점 vs 판매량 관계",
            labels={'Critic_Score': '평점 (Metacritic)', 'Global_Sales': '판매량 (백만 단위)'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        # 평점 분포
        fig_hist = px.histogram(
            filtered_df,
            x='Critic_Score',
            nbins=20,
            title="📊 게임 평점 분포",
            labels={'Critic_Score': '평점', 'count': '게임 수'}
        )
        fig_hist.update_traces(marker_color='lightseagreen')
        st.plotly_chart(fig_hist, use_container_width=True)

# ============================================
# TAB 5: 순위
# ============================================
with tab5:
    st.subheader("🏆 순위")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**상위 10개 게임 (판매량)**")
        top_games = filtered_df.nlargest(10, 'Global_Sales')[['Name', 'Platform', 'Year_of_Release', 'Global_Sales', 'Critic_Score']]
        top_games_display = top_games.copy()
        top_games_display.columns = ['게임명', '플랫폼', '연도', '판매량(M)', '평점']
        st.dataframe(top_games_display, use_container_width=True)

    with col2:
        st.write("**상위 10개 게임 (평점)**")
        top_rated = filtered_df.nlargest(10, 'Critic_Score')[['Name', 'Platform', 'Year_of_Release', 'Global_Sales', 'Critic_Score']]
        top_rated_display = top_rated.copy()
        top_rated_display.columns = ['게임명', '플랫폼', '연도', '판매량(M)', '평점']
        st.dataframe(top_rated_display, use_container_width=True)

# ============================================
# 푸터
# ============================================
st.markdown("---")
st.markdown("**데이터 출처:** Kaggle - Video Game Sales with Ratings")
st.markdown("**데이터 기준:** 2016년 12월 22일")
st.markdown("**프로젝트:** 게임 판매 데이터 분석 대쉬보드 (Streamlit)")
