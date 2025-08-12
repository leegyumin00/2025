import streamlit as st

st.set_page_config(layout="centered", # 페이지 레이아웃 설정
                   initial_sidebar_state="expanded") # 사이드바 초기 상태 설정

# 디자인 콘셉트 - 무채색 기반 + 포인트 컬러 예시
# Streamlit은 직접 CSS를 적용하기 어렵지만, markdown 등으로 스타일을 조절할 수 있어요.
# st.markdown("""
# <style>
# .main {
#     background-color: #f0f2f6; # 라이트 그레이 배경
#     color: #333333; # 다크 그레이 텍스트
# }
# .stButton>button {
#     background-color: #4CAF50; # 녹색 버튼 (포인트 컬러)
#     color: white;
# }
# </style>
# """, unsafe_allow_html=True)

mbti_jobs = {
    "ISTP": ["정비사", "엔지니어", "건축가", "컴퓨터 기술자"],
    "ISFP": ["그래픽 디자이너", "패션 디자이너", "예술가", "요리사"],
    "INFP": ["작가", "심리학자/치료사", "편집자"],
    "ENFP": ["크리에이티브 디렉터", "디자이너", "방송 프로듀서", "상담사"],
    "INTJ": ["투자 은행가", "소프트웨어 개발자", "경제학자"],
    "INFJ": ["치료사/상담사", "사회 복지사"],
    "ENTP": ["기업가", "컨설턴트", "발명가", "기획자", "변호사", "마케터"] # ENTP는 누나의 MBTI죠!
}

st.title("💖 나의 MBTI와 어울리는 직업 찾기 💖")
st.markdown("---") # 무채색 배경에 대비되는 라인으로 분리

st.write("초등학교 교사를 꿈꾸는 누나를 위한 진로 탐색 도우미예요!")

# MBTI 유형 선택
selected_mbti = st.selectbox(
    "✨ 나의 MBTI 유형을 선택해보세요!",
    [""] + sorted(list(mbti_jobs.keys())) # 선택지 정렬
)

if selected_mbti:
    st.subheader(f"💡 당신은 `{selected_mbti}`! 이 유형에 어울리는 직업을 추천해요.")
    recommended_jobs = mbti_jobs.get(selected_mbti, ["아직 준비된 직업 추천이 없어요! 😢"])
    for job in recommended_jobs:
        st.markdown(f"- **{job}**") # 추천 직업 목록을 강조해서 보여주기
