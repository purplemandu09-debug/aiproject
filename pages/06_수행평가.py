# 06_수행평가.py

from pathlib import Path
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ====================================
# 기본 설정
# ====================================

st.set_page_config(
    page_title="전국 해파리 발생·예보 통합 시스템",
    page_icon="🪼",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

SEA_FILE = BASE_DIR / "sea.csv"
SEA02_FILE = BASE_DIR / "sea02.csv"

# ====================================
# 관측 데이터
# ====================================

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

    return df


# ====================================
# 뉴스 데이터
# ====================================

@st.cache_data
def load_news():

    rows = []

    for enc in ["cp949", "euc-kr", "utf-8"]:

        try:

            with open(
                SEA02_FILE,
                "r",
                encoding=enc
            ) as f:

                for line in f:

                    line = line.strip()

                    if not line:
                        continue

                    parts = line.split("\t", 1)

                    if len(parts) == 2:

                        rows.append({
                            "날짜": parts[0],
                            "내용": parts[1]
                        })

                    else:

                        rows.append({
                            "날짜": "",
                            "내용": line
                        })

            break

        except Exception:
            continue

    news = pd.DataFrame(rows)

    news["날짜"] = news["날짜"].astype(str)
    news["내용"] = news["내용"].astype(str)

    return news

# ====================================
# 파일 체크
# ====================================

if not SEA_FILE.exists():
    st.error(f"sea.csv 없음\n{SEA_FILE}")
    st.stop()

if not SEA02_FILE.exists():
    st.error(f"sea02.csv 없음\n{SEA02_FILE}")
    st.stop()

obs = load_observation()
news = load_news()

# ====================================
# 제목
# ====================================

st.title("🪼 전국 해파리 발생·예보 통합 시스템")
st.caption("관측 데이터 + 예보 뉴스 데이터")

# ====================================
# 사이드바
# ====================================

years = sorted(
    obs["연도"].dropna().unique()
)

selected_year = st.sidebar.selectbox(
    "연도 선택",
    ["전체"] + list(years)
)

filtered = obs.copy()

if selected_year != "전체":
    filtered = filtered[
        filtered["연도"] == selected_year
    ]

# ====================================
# KPI
# ====================================

st.subheader("📊 현황 요약")

c1, c2, c3 = st.columns(3)

c1.metric("관측 건수", len(filtered))
c2.metric("관측 지역", filtered["지역"].nunique())
c3.metric("뉴스 건수", len(news))

st.divider()

# ====================================
# 지도
# ====================================

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

        folium.CircleMarker(
            location=[
                row["위도"],
                row["경도"]
            ],
            radius=4,
            color="blue",
            fill=True,
            fill_color="blue"
        ).add_to(m)

    st_folium(
        m,
        width=900,
        height=500
    )

st.divider()

# ====================================
# 월별 발생
# ====================================

st.subheader("📈 월별 발생 현황")

monthly = (
    filtered.groupby("월")
    .size()
    .reset_index(name="발생건수")
)

if len(monthly):

    st.line_chart(
        monthly.set_index("월")
    )

st.divider()

# ====================================
# TOP10
# ====================================

st.subheader("🏖️ 발생 지역 TOP10")

top_region = (
    filtered["지역"]
    .value_counts()
    .head(10)
)

st.bar_chart(top_region)

st.divider()

# ====================================
# 위험도
# ====================================

st.subheader("🚨 전국 위험도")

news_text = "\n".join(
    news["내용"].fillna("").astype(str)
)

danger = (
    news_text.count("주의경보")
    + news_text.count("주의보")
    + news_text.count("대량출현")
    + news_text.count("대량 발생")
    + news_text.count("어업피해")
)

if danger > 50:
    level = "🔴 위험"
elif danger > 20:
    level = "🟡 주의"
else:
    level = "🟢 안전"

st.metric("현재 위험도", level)
st.write(f"위험 키워드 수 : {danger}")

# ====================================
# 해파리 종 분석
# ====================================

species = [
    "노무라입깃해파리",
    "보름달물해파리",
    "작은상자해파리",
    "유령해파리"
]

species_df = pd.DataFrame({
    "종류": species,
    "출현횟수": [
        news_text.count(x)
        for x in species
    ]
})

st.subheader("🪼 주요 해파리 출현")

st.bar_chart(
    species_df.set_index("종류")
)

st.divider()

# ====================================
# 뉴스 검색
# ====================================

if keyword:st.text_input(...)

    result = news[
        news["내용"]
        .fillna("")
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
# ====================================
# 최근 뉴스
# ====================================
st.subheader("📰 최근 뉴스")

for i in range(
    min(10, len(news))
):

    with st.expander(
        str(news.iloc[i]["날짜"])
    ):

        st.write(
            news.iloc[i]["내용"]
        )

# ====================================
# 원본 데이터
# ====================================

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
