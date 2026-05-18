import streamlit as st

st.set_page_config(
    page_title="✨ MBTI 진로 추천기",
    page_icon="🌈",
    layout="centered"
)

# MBTI별 진로 데이터
career_data = {
    "INTJ": [
        {
            "job": "🧠 데이터 사이언티스트",
            "major": "컴퓨터공학과, 통계학과",
            "personality": "논리적이고 분석하는 걸 좋아하는 성격!",
            "salary": "평균 연봉 약 5,500만 원"
        },
        {
            "job": "🚀 전략기획가",
            "major": "경영학과, 경제학과",
            "personality": "미래를 계획하고 문제 해결을 잘하는 타입!",
            "salary": "평균 연봉 약 5,000만 원"
        }
    ],

    "INTP": [
        {
            "job": "💻 프로그래머",
            "major": "소프트웨어학과, 컴퓨터공학과",
            "personality": "호기심 많고 새로운 아이디어를 좋아함!",
            "salary": "평균 연봉 약 5,200만 원"
        },
        {
            "job": "🔬 연구원",
            "major": "물리학과, 화학과",
            "personality": "깊게 탐구하는 걸 즐기는 성격!",
            "salary": "평균 연봉 약 4,800만 원"
        }
    ],

    "ENTJ": [
        {
            "job": "📈 CEO / 경영자",
            "major": "경영학과",
            "personality": "리더십 강하고 목표 지향적!",
            "salary": "평균 연봉 약 6,000만 원"
        },
        {
            "job": "⚖️ 변호사",
            "major": "법학과",
            "personality": "논리적이고 추진력이 강함!",
            "salary": "평균 연봉 약 7,000만 원"
        }
    ],

    "ENTP": [
        {
            "job": "🎤 마케팅 기획자",
            "major": "광고홍보학과",
            "personality": "아이디어가 넘치고 창의적!",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "📺 콘텐츠 크리에이터",
            "major": "미디어학과",
            "personality": "새로운 도전을 즐기는 타입!",
            "salary": "평균 연봉 약 4,000만 원"
        }
    ],

    "INFJ": [
        {
            "job": "🩺 상담심리사",
            "major": "심리학과",
            "personality": "공감 능력이 뛰어나고 배려심 많음!",
            "salary": "평균 연봉 약 4,200만 원"
        },
        {
            "job": "✍️ 작가",
            "major": "문예창작과",
            "personality": "감수성이 풍부하고 상상력이 뛰어남!",
            "salary": "평균 연봉 약 3,800만 원"
        }
    ],

    "INFP": [
        {
            "job": "🎨 디자이너",
            "major": "디자인학과",
            "personality": "감성적이고 창의적인 성격!",
            "salary": "평균 연봉 약 4,300만 원"
        },
        {
            "job": "📚 웹소설 작가",
            "major": "문예창작과",
            "personality": "상상력 풍부하고 자유로운 타입!",
            "salary": "평균 연봉 약 3,500만 원"
        }
    ],

    "ENFJ": [
        {
            "job": "👩‍🏫 교사",
            "major": "교육학과",
            "personality": "사람들을 이끄는 걸 좋아함!",
            "salary": "평균 연봉 약 4,800만 원"
        },
        {
            "job": "🤝 HR 담당자",
            "major": "경영학과",
            "personality": "소통 능력이 뛰어나고 친화력 좋음!",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ],

    "ENFP": [
        {
            "job": "🎬 방송 PD",
            "major": "미디어학과",
            "personality": "에너지 넘치고 창의적!",
            "salary": "평균 연봉 약 4,700만 원"
        },
        {
            "job": "🌟 이벤트 기획자",
            "major": "관광경영학과",
            "personality": "사람들과 어울리는 걸 좋아함!",
            "salary": "평균 연봉 약 4,200만 원"
        }
    ],

    "ISTJ": [
        {
            "job": "🏦 회계사",
            "major": "회계학과",
            "personality": "꼼꼼하고 책임감 강함!",
            "salary": "평균 연봉 약 6,000만 원"
        },
        {
            "job": "👮 경찰관",
            "major": "경찰행정학과",
            "personality": "원칙을 중요하게 생각하는 타입!",
            "salary": "평균 연봉 약 4,800만 원"
        }
    ],

    "ISFJ": [
        {
            "job": "💉 간호사",
            "major": "간호학과",
            "personality": "배려심 많고 성실함!",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "🏫 사회복지사",
            "major": "사회복지학과",
            "personality": "남을 돕는 걸 좋아함!",
            "salary": "평균 연봉 약 3,800만 원"
        }
    ],

    "ESTJ": [
        {
            "job": "📊 공무원",
            "major": "행정학과",
            "personality": "체계적이고 책임감이 강함!",
            "salary": "평균 연봉 약 4,700만 원"
        },
        {
            "job": "🏢 프로젝트 매니저",
            "major": "경영학과",
            "personality": "리더십과 추진력이 뛰어남!",
            "salary": "평균 연봉 약 5,500만 원"
        }
    ],

    "ESFJ": [
        {
            "job": "✈️ 승무원",
            "major": "항공서비스학과",
            "personality": "친절하고 사교성이 좋음!",
            "salary": "평균 연봉 약 4,600만 원"
        },
        {
            "job": "🛍️ 서비스 매니저",
            "major": "호텔관광학과",
            "personality": "사람 챙기는 걸 좋아함!",
            "salary": "평균 연봉 약 4,300만 원"
        }
    ],

    "ISTP": [
        {
            "job": "🔧 엔지니어",
            "major": "기계공학과",
            "personality": "손으로 만드는 걸 좋아함!",
            "salary": "평균 연봉 약 5,300만 원"
        },
        {
            "job": "🛩️ 파일럿",
            "major": "항공운항학과",
            "personality": "침착하고 상황 판단이 빠름!",
            "salary": "평균 연봉 약 7,000만 원"
        }
    ],

    "ISFP": [
        {
            "job": "📷 사진작가",
            "major": "사진영상학과",
            "personality": "감각적이고 자유로운 스타일!",
            "salary": "평균 연봉 약 3,700만 원"
        },
        {
            "job": "🎵 음악 프로듀서",
            "major": "실용음악과",
            "personality": "예술 감각이 뛰어남!",
            "salary": "평균 연봉 약 4,200만 원"
        }
    ],

    "ESTP": [
        {
            "job": "💼 영업 전문가",
            "major": "경영학과",
            "personality": "활동적이고 도전 정신이 강함!",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "🎮 e스포츠 코치",
            "major": "스포츠학과",
            "personality": "순발력 좋고 경쟁을 즐김!",
            "salary": "평균 연봉 약 4,000만 원"
        }
    ],

    "ESFP": [
        {
            "job": "🎤 연예인 / 방송인",
            "major": "연극영화과",
            "personality": "사람들 앞에서 빛나는 타입!",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "🍰 파티시에",
            "major": "제과제빵학과",
            "personality": "즐겁고 감각적인 성격!",
            "salary": "평균 연봉 약 3,900만 원"
        }
    ]
}

# 제목
st.title("🌈 MBTI 진로 추천기")
st.write("너의 MBTI에 딱 맞는 진로를 추천해줄게 😎")

# MBTI 선택
mbti = st.selectbox(
    "👉 너의 MBTI를 선택해봐!",
    list(career_data.keys())
)

# 버튼
if st.button("✨ 진로 추천 받기"):
    st.success(f"{mbti} 유형에게 잘 어울리는 진로야!")

    careers = career_data[mbti]

    for idx, career in enumerate(careers, start=1):
        st.markdown(f"---")
        st.subheader(f"{idx}. {career['job']}")

        st.write(f"📚 추천 학과 : {career['major']}")
        st.write(f"💖 잘 맞는 성격 : {career['personality']}")
        st.write(f"💰 평균 연봉 : {career['salary']}")

    st.balloons()

st.markdown("---")
st.caption("🌟 재미로 보는 진로 추천이니까 부담 없이 즐겨봐!")
