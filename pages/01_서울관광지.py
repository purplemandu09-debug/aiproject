import streamlit as st
    {
        "name": "명동 🛍️",
        "lat": 37.5636,
        "lon": 126.9827,
        "desc": "쇼핑과 길거리 음식의 천국"
    },
    {
        "name": "북촌한옥마을 🏡",
        "lat": 37.5826,
        "lon": 126.9830,
        "desc": "전통 한옥 감성 명소"
    },
    {
        "name": "홍대 🎵",
        "lat": 37.5563,
        "lon": 126.9220,
        "desc": "젊음과 공연 문화의 거리"
    },
    {
        "name": "동대문디자인플라자(DDP) ✨",
        "lat": 37.5665,
        "lon": 127.0092,
        "desc": "미래적인 건축물과 전시 공간"
    },
    {
        "name": "롯데월드 🎡",
        "lat": 37.5110,
        "lon": 127.0980,
        "desc": "서울 대표 테마파크"
    },
    {
        "name": "한강공원 🚴",
        "lat": 37.5206,
        "lon": 126.9408,
        "desc": "피크닉과 자전거 명소"
    },
    {
        "name": "인사동 🎨",
        "lat": 37.5740,
        "lon": 126.9850,
        "desc": "전통 문화와 기념품 거리"
    },
    {
        "name": "코엑스 별마당도서관 📚",
        "lat": 37.5125,
        "lon": 127.0589,
        "desc": "SNS 인기 실내 관광지"
    }
]

# 마커 추가
for place in places:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=f"<b>{place['name']}</b><br>{place['desc']}",
        tooltip=place["name"],
        icon=folium.Icon(color="blue", icon="star")
    ).add_to(seoul_map)

# 지도 출력
st_folium(seoul_map, width=1200, height=700)

st.markdown("---")
st.caption("Made with ❤️ using Streamlit & Folium")
