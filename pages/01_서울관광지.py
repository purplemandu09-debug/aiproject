import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 관광지 TOP10",
    page_icon="🗺️",
    layout="wide"
)

# 제목
st.title("🗺️ 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("서울의 인기 관광지를 지도에서 확인해보세요! ✨")

# 서울 중심 지도 생성
seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11
)

# 관광지 데이터
places = [
    ["경복궁 🏯", 37.5796, 126.9770, "조선 시대 대표 궁궐"],
    ["남산서울타워 🌃", 37.5512, 126.9882, "서울 야경 명소"],
    ["명동 🛍️", 37.5636, 126.9827, "쇼핑과 길거리 음식"],
    ["북촌한옥마을 🏡", 37.5826, 126.9830, "전통 한옥 감성"],
    ["홍대 🎵", 37.5563, 126.9220, "젊음과 공연 문화"],
    ["DDP ✨", 37.5665, 127.0092, "미래형 건축물"],
    ["롯데월드 🎡", 37.5110, 127.0980, "대표 테마파크"],
    ["한강공원 🚴", 37.5206, 126.9408, "피크닉 명소"],
    ["인사동 🎨", 37.5740, 126.9850, "전통 문화 거리"],
    ["별마당도서관 📚", 37.5125, 127.0589, "SNS 인기 명소"]
]

# 마커 추가
for place in places:
    folium.Marker(
        location=[place[1], place[2]],
        popup=f"<b>{place[0]}</b><br>{place[3]}",
        tooltip=place[0],
        icon=folium.Icon(color="blue", icon="star")
    ).add_to(seoul_map)

# 지도 출력
st_folium(seoul_map, width=1200, height=700)

st.markdown("---")
st.caption("Made with ❤️ using Streamlit & Folium")
