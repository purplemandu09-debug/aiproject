import streamlit as st
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import st_folium
import re

st.set_page_config(
    page_title="전국 해파리 발생·예보 통합 시스템",
    page_icon="🪼",
    layout="wide"
)

# =====================================================
# 데이터 로드
# =====================================================

@st.cache_data
def load_observation():

    try:
        df = pd.read_csv("sea.csv", encoding="cp949")
    except:
        df = pd.read_csv("sea.csv", encoding="euc-kr")

    df["보고일자"] = pd.to_datetime(
        df["보고일자"],
        errors="coerce"
    )

    df["연도"] = df["보고일자"].dt.year
    df["월"] = df["보고일자"].dt.month

    df = df.dropna(
        subset=["위도", "경도"]
    )

    return df


@st.cache_data
def load_news():

    try:
        news = pd.read_csv(
            "sea02.csv",
            encoding="cp949"
        )
    except:
        news = pd.read_csv(
            "sea02.csv",
            encoding="euc-kr"
        )

    return news


obs = load_observation()
news = load_news()

# =====================================================
# 제목
# =====================================================

st.title("🪼 전국 해파리 발생·예보 통합 시스템")
st.caption("관측 데이터 + 주간 예보 데이터 통합")

# =====================================================
# 사이드바
# =====================================================

st.sidebar.header("검색 옵션")

years = sorted(
    obs["연도"]
    .dropna()
    .unique()
)

selected_year = st.sidebar.selectbox(
    "연도",
    ["전체"] + list(years)
)

dense_only = st.sidebar.checkbox(
    "밀집지역만 보기"
)

# =====================================================
# 필터
# =====================================================

filtered = obs.copy()

if selected_year != "전체":
    filtered = filtered[
        filtered["연도"] == selected_year
    ]

if dense_only:
    filtered = filtered[
        filtered["밀집여부"] == "y"
    ]

# =====================================================
# KPI
# =====================================================

st.subheader("📊 현황 요약")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "관측건수",
    f"{len(filtered):,}"
)

c2.metric(
    "관측지역",
    filtered["지역"].nunique()
)

c3.metric(
    "밀집지역",
    len(filtered[
        filtered["밀집여부"] == "y"
    ])
)

c4.metric(
    "뉴스건수",
    len(news)
)

st.divider()

# =====================================================
# 지도
# =====================================================

st.subheader("🗺️ 전국 해파리 발생 지도")

lat = filtered["위도"].mean()
lon = filtered["경도"].mean()

m = folium.Map(
    location=[lat, lon],
    zoom_start=7
)

sample_df = filtered.sample(
    min(len(filtered), 3000),
    random_state=42
)

for _, row in sample_df.iterrows():

    popup = f"""
    지역 : {row['지역']}<br>
    날짜 : {row['보고일자']}<br>
    크기 : {row['해파리크기']}<br>
    밀집 : {row['밀집여부']}
    """

    folium.CircleMarker(
        location=[
            row["위도"],
            row["경도"]
        ],
        radius=4,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.7,
        popup=popup
    ).add_to(m)

col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    st_folium(
        m,
        width=1000,
        height=600
    )

st.divider()

# =====================================================
# 월별 통계
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("📈 월별 발생 현황")

    monthly = (
        filtered.groupby("월")
        .size()
        .reset_index(name="발생건수")
    )

    fig = px.line(
        monthly,
        x="월",
        y="발생건수",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("🏖️ 발생지역 TOP10")

    top_region = (
        filtered["지역"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_region.columns = [
        "지역",
        "발생건수"
    ]

    fig2 = px.bar(
        top_region,
        x="발생건수",
        y="지역",
        orientation="h"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# =====================================================
# 뉴스 분석
# =====================================================

st.subheader("📰 해파리 예보 및 뉴스")

news_text = "\n".join(
    news.iloc[:, 1].astype(str)
)

danger_score = 0

danger_score += news_text.count("주의경보")
danger_score += news_text.count("대량발생")
danger_score += news_text.count("쏘임사고")

if danger_score > 50:
    level = "🔴 위험"
elif danger_score > 20:
    level = "🟡 주의"
else:
    level = "🟢 안전"

st.metric(
    "전국 위험도",
    level
)

st.write(
    f"위험 키워드 탐지 수 : {danger_score}"
)

# =====================================================
# 해파리 종 분석
# =====================================================

st.subheader("🪼 뉴스에 등장한 주요 해파리")

species = [
    "노무라입깃해파리",
    "보름달물해파리",
    "두빛보름달해파리",
    "작은상자해파리",
    "유령해파리",
    "작은부레관해파리",
    "꽃모자갈퀴손해파리",
    "야광원양해파리",
]

species_count = []

for s in species:
    species_count.append(
        news_text.count(s)
    )

species_df = pd.DataFrame({
    "종류": species,
    "출현횟수": species_count
})

fig3 = px.bar(
    species_df,
    x="종류",
    y="출현횟수"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

# =====================================================
# 뉴스 검색
# =====================================================

st.subheader("🔎 뉴스 검색")

keyword = st.text_input(
    "지역 또는 해파리 이름 입력"
)

if keyword:

    result = news[
        news.iloc[:, 1]
        .astype(str)
        .str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

    st.write(
        f"검색 결과 : {len(result)}건"
    )

    st.dataframe(
        result,
        use_container_width=True
    )

st.divider()

# =====================================================
# 최근 뉴스
# =====================================================

st.subheader("📋 최근 뉴스")

for i in range(
    min(10, len(news))
):
    with st.expander(
        f"뉴스 {i+1}"
    ):
        st.write(
            news.iloc[i, 1]
        )

# =====================================================
# 원본 데이터
# =====================================================

with st.expander(
    "📂 관측 데이터 보기"
):
    st.dataframe(
        filtered,
        use_container_width=True
    )

with st.expander(
    "📂 뉴스 데이터 보기"
):
    st.dataframe(
        news,
        use_container_width=True
    )
