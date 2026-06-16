# 06_수행평가.py

from pathlib import Path
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ==========================
# 기본 설정
# ==========================

st.set_page_config(
    page_title="전국 해파리 발생·예보 통합 시스템",
    page_icon="🪼",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

SEA_FILE = BASE_DIR / "sea.csv"
SEA02_FILE = BASE_DIR / "sea02.csv"

# ==========================
# 데이터 로드
# ==========================

@st.cache_data
def load_observation():

    try:
        df = pd.read_csv(SEA_FILE, encoding="cp949")
    except:
        df = pd.read_csv(SEA_FILE, encoding="euc-kr")

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
            SEA02_FILE,
            sep="\t",
            header=None,
            encoding="cp949"
        )
    except:
        news = pd.read_csv(
            SEA02_FILE,
            sep="\t",
            header=None,
            encoding="euc-kr"
        )

    if len(news.columns) >= 2:
        news.columns = ["날짜", "내용"]

    return news


# ==========================
# 파일 존재 확인
# ==========================

if not SEA_FILE.exists():
    st.error(f"sea.csv 파일이 없습니다.\n{SEA_FILE}")
    st.stop()

if not SEA02_FILE.exists():
    st.error(f"sea02.csv 파일이 없습니다.\n{SEA02_FILE}")
    st.stop()

obs = load_observation()
news = load_news()

# ==========================
# 제목
# ==========================

st.title("🪼 전국 해파리 발생·예보 통합 시스템")
st.caption("관측 데이터 + 예보 뉴스 데이터 통합")

# ==========================
# 사이드바
# ==========================

st.sidebar.header("검색 옵션")

years = sorted(
    obs["연도"]
    .dropna()
    .unique()
)

selected_year = st.sidebar.selectbox(
    "연도 선택",
    ["전체"] + list(years)
)

# ==========================
# 필터
# ==========================

filtered = obs.copy()

if selected_year != "전체":
    filtered = filtered[
        filtered["연도"] == selected_year
    ]

# ==========================
# KPI
# ==========================

st.subheader("📊 현황 요약")

c1, c2, c3 = st.columns(3)

c1.metric("관측 건수", len(filtered))
c2.metric("관측 지역 수", filtered["지역"].nunique())
c3.metric("뉴스 건수", len(news))

st.divider()

# ==========================
# 지도
# ==========================

st.subheader("🗺️ 해파리 발생 지도")

if len(filtered) > 0:

    lat = filtered["위도"].mean()
    lon = filtered["경도"].mean()

    m = folium.Map(
        location=[lat, lon],
        zoom_start=7
    )

    sample = filtered.head(1000)

    for _, row in sample.iterrows():

        popup = f"""
        지역 : {row['지역']}<br>
        날짜 : {row['보고일자']}<br>
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
            popup=popup
        ).add_to(m)

    st_folium(
        m,
        width=900,
        height=500
    )

st.divider()

# ==========================
# 월별 발생 현황
# ==========================

st.subheader("📈 월별 발생 현황")

monthly = (
    filtered.groupby("월")
    .size()
    .reset_index(name="발생건수")
)

if len(monthly) > 0:

    monthly = monthly.set_index("월")

    st.line_chart(
        monthly["발생건수"]
    )

st.divider()

# ==========================
# 발생 지역 TOP10
# ==========================

st.subheader("🏖️ 발생 지역 TOP10")

top_region = (
    filtered["지역"]
    .value_counts()
    .head(10)
)

st.bar_chart(top_region)

st.divider()

# ==========================
# 위험도 분석
# ==========================

st.subheader("🚨 전국 위험도")

news_text = "\n".join(
    news.iloc[:, -1].astype(str)
)

danger = (
    news_text.count("주의경보")
    + news_text.count("대량발생")
    + news_text.count("쏘임사고")
)

if danger > 50:
    level = "🔴 위험"
elif danger > 20:
    level = "🟡 주의"
else:
    level = "🟢 안전"

st.metric(
    "현재 위험도",
    level
)

st.write(
    f"위험 키워드 발견 수 : {danger}"
)

st.divider()

# ==========================
# 해파리 종류 분석
# ==========================

species = [
    "노무라입깃해파리",
    "보름달물해파리",
    "두빛보름달해파리",
    "작은상자해파리",
    "유령해파리"
]

count_list = []

for s in species:
    count_list.append(
        news_text.count(s)
    )

species_df = pd.DataFrame({
    "종류": species,
    "출현횟수": count_list
})

st.subheader("🪼 주요 해파리 출현")

st.bar_chart(
    species_df.set_index("종류")
)

st.divider()

# ==========================
# 뉴스 검색
# ==========================

st.subheader("🔍 뉴스 검색")

keyword = st.text_input(
    "지역 또는 해파리 이름"
)

if keyword:

    result = news[
        news.iloc[:, -1]
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

# ==========================
# 최근 뉴스
# ==========================

st.subheader("📰 최근 뉴스")

for i in range(min(10, len(news))):

    with st.expander(
        f"뉴스 {i+1}"
    ):
        st.write(
            news.iloc[i, -1]
        )

# ==========================
# 원본 데이터
# ==========================

with st.expander("📂 관측 데이터"):
    st.dataframe(
        filtered,
        use_container_width=True
    )

with st.expander("📂 뉴스 데이터"):
    st.dataframe(
        news,
        use_container_width=True
    )
