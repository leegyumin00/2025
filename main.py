import streamlit as st

# 페이지 설정 (레이아웃, 초기 사이드바 상태 등)
st.set_page_config(
    page_title="💖 나의 MBTI와 어울리는 직업 찾기 💖",
    layout="centered", # 'wide'로 하면 페이지가 넓게 사용됨
    initial_sidebar_state="expanded" # 사이드바를 초기부터 열린 상태로
)

# --- 디자인 콘셉트: 무채색 기반 + 포인트 컬러 (Streamlit에서 CSS 직접 적용은 제한적이라, Markdown으로 최대한 구현) ---
# 무채색 배경, 텍스트 컬러 설정
# Streamlit은 사용자 지정 CSS를 직접 적용하기 어렵지만, markdown의 unsafe_allow_html=True를 사용하여 일부 스타일을 조절할 수 있어.
# 하지만 전체적인 배경 색상은 Streamlit 테마 설정이나 config.toml 파일을 통해 하는 것이 더 권장돼.
# 여기서는 Streamlit의 기본 테마를 활용하고, 특정 요소에 대한 색상 강조만 markdown으로 시도해볼게.
st.markdown("""
<style>
    /* 전체 배경은 Streamlit 기본 테마 (라이트 모드면 흰색, 다크 모드면 어두운 회색) */
    /* 텍스트는 무채색 계열로 */
    body {
        color: #333333; /* 진한 회색 */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #222222; /* 더 진한 회색 */
    }
    /* 특정 버튼이나 강조하고 싶은 부분에 포인트 컬러 적용 예시 (Streamlit 기본 버튼 색상을 따름) */
    /* st.selectbox와 같은 위젯은 스타일을 직접 바꾸기 어려움 */
</style>
""", unsafe_allow_html=True)


# MBTI 유형별 직업 및 간단한 설명 딕셔너리
# (직업 설명은 검색 기반으로 요약해서 추가함)
mbti_jobs_with_descriptions = {
    "ISTJ": [
        {"name": "회계사", "description": "기업이나 개인의 재무 기록을 관리하고 분석하여 재무 상태를 보고하는 전문가."},
        {"name": "경찰관", "description": "법을 집행하고 공공의 질서를 유지하며 범죄를 예방하는 직업."},
        {"name": "행정 공무원", "description": "국가나 지방 공공 기관에서 행정 업무를 수행하며 공공 서비스를 제공하는 직업."}
    ],
    "ISFJ": [
        {"name": "간호사", "description": "환자 치료와 건강 관리를 돕고 의료진과 협력하는 보건 의료 전문가."},
        {"name": "사회복지사", "description": "사회적, 개인적 어려움을 겪는 사람들을 돕고 복지 서비스를 연계하는 직업."},
        {"name": "초등학교 교사", "description": "어린 학생들을 가르치고 지도하며 전인적인 성장을 돕는 교육자."}
    ],
    "INFJ": [
        {"name": "심리학자", "description": "인간의 행동과 심리 과정을 연구하고 심리 상담을 제공하는 전문가."},
        {"name": "상담사", "description": "개인의 고민이나 문제를 듣고 해결 방안을 함께 모색하며 조언을 제공하는 직업."},
        {"name": "작가", "description": "다양한 형식의 글을 창작하여 독자에게 정보를 전달하거나 감동을 주는 직업."}
    ],
    "INTJ": [
        {"name": "과학자", "description": "자연 현상이나 특정 분야를 깊이 연구하여 새로운 지식을 발견하는 학자."},
        {"name": "엔지니어", "description": "과학 기술을 활용하여 제품, 시스템, 구조물 등을 설계하고 개발하는 직업."},
        {"name": "IT 개발자", "description": "소프트웨어나 애플리케이션을 기획, 설계, 개발하고 유지 보수하는 전문가."}
    ],
    "ISTP": [ # [【2】](https://brunch.co.kr/@inplanet/16)
        {"name": "정비사", "description": "기계나 장치의 고장을 진단하고 수리하며, 정상 작동하도록 유지하는 전문가."},
        {"name": "목수", "description": "나무를 이용하여 건축물이나 가구를 제작하고 수리하는 기술자."},
        {"name": "경찰특공대", "description": "특수 작전이나 긴급 상황에 투입되어 인명 구조 및 범죄 진압을 수행하는 요원."}
    ],
    "ISFP": [ # [【2】](https://brunch.co.kr/@inplanet/16) 
        {"name": "그래픽 디자이너", "description": "시각적 요소들을 조합하여 메시지를 전달하는 디자인 전문가."},
        {"name": "패션 디자이너", "description": "의류, 액세서리 등을 디자인하고 제작하여 새로운 스타일을 창조하는 직업."},
        {"name": "예술가", "description": "자신의 생각과 감정을 그림, 음악, 조각 등 예술 작품으로 표현하는 사람."}
    ],
    "INFP": [ # [【2】](https://brunch.co.kr/@inplanet/16) 
        {"name": "작가", "description": "다양한 분야에서 글을 쓰고 창작하여 정보를 전달하거나 감동을 주는 직업."},
        {"name": "심리학자", "description": "인간의 마음과 행동을 연구하고 정신 건강 상담을 제공하는 전문가."},
        {"name": "사서", "description": "도서관의 자료를 체계적으로 관리하고 이용자에게 정보 서비스를 제공하는 직업."}
    ],
    "INTP": [
        {"name": "교수", "description": "대학에서 특정 학문을 가르치고 연구하며 학생들을 지도하는 교육자."},
        {"name": "컴퓨터 프로그래머", "description": "컴퓨터 언어를 사용하여 소프트웨어와 프로그램을 개발하는 전문가."},
        {"name": "데이터 과학자", "description": "대규모 데이터를 분석하여 의미 있는 통찰을 도출하고 비즈니스 문제를 해결하는 전문가."}
    ],
    "ESTP": [
        {"name": "세일즈맨", "description": "제품이나 서비스를 고객에게 판매하고 고객과의 관계를 구축하는 직업."},
        {"name": "기업가", "description": "새로운 사업 아이디어를 실행하고 비즈니스를 운영하며 위험을 감수하는 사람."},
        {"name": "레크레이션 강사", "description": "다양한 활동을 통해 사람들에게 즐거움과 휴식을 제공하는 전문가."}
    ],
    "ESFP": [
        {"name": "연예인", "description": "가수, 배우 등 대중 매체를 통해 사람들에게 즐거움을 선사하는 직업."},
        {"name": "이벤트 플래너", "description": "각종 행사나 파티를 기획하고 실행하여 성공적인 이벤트를 만드는 전문가."},
        {"name": "강사", "description": "특정 분야의 지식이나 기술을 사람들에게 가르치고 교육하는 직업."}
    ],
    "ENFP": [ # [【3】](https://www.jobkorea.co.kr/goodjob/tip/view?News_No=18406)
        {"name": "크리에이티브 디렉터", "description": "광고, 미디어 콘텐츠 등 창의적인 작업의 총괄 기획자."},
        {"name": "카운슬러", "description": "개인의 심리적 어려움을 돕고 삶의 질을 향상시키기 위한 조언을 제공하는 전문가."},
        {"name": "상품 기획자", "description": "시장의 요구를 분석하여 새로운 제품이나 서비스를 기획하고 개발하는 직업."}
    ],
    "ENTP": [ # 누나의 MBTI! 혁신과 토론을 즐기는 변론가 성향이야. [【1】](https://www.jobkorea.co.kr/goodjob/tip/view?News_No=18406) [【4】](https://blog.naver.com/with_yjc/223416311931)
        {"name": "기업가", "description": "새로운 사업 아이디어를 발굴하고 실행하여 비즈니스를 창조하는 사람."},
        {"name": "발명가", "description": "기존에 없던 새로운 기술이나 제품을 개발하여 세상에 선보이는 직업."},
        {"name": "컨설턴트", "description": "전문 지식을 바탕으로 기업이나 개인의 문제점을 진단하고 해결책을 제시하는 전문가."},
        {"name": "변호사", "description": "법률 전문가로서 의뢰인의 권리를 옹호하고 법적 분쟁을 해결하는 직업."},
        {"name": "마케터", "description": "제품이나 서비스를 소비자에게 알리고 판매를 촉진하는 전략을 세우는 전문가."}
    ],
    "ESTJ": [
        {"name": "프로젝트 매니저", "description": "프로젝트의 목표 달성을 위해 계획, 실행, 관리를 총괄하는 책임자."},
        {"name": "변호사", "description": "법률 전문가로서 의뢰인의 권리를 옹호하고 법적 분쟁을 해결하는 직업."},
        {"name": "경영 컨설턴트", "description": "기업의 경영 문제를 진단하고 개선 방안을 제시하는 전문가."}
    ],
    "ESFJ": [
        {"name": "영업 관리자", "description": "영업팀을 이끌고 영업 목표를 달성하기 위한 전략을 수립하는 관리자."},
        {"name": "인사 관리자", "description": "직원 채용, 교육, 평가 등 인적 자원 관리를 담당하는 전문가."},
        {"name": "승무원", "description": "항공기나 선박에서 승객의 안전과 편의를 담당하는 서비스 직업."}
    ],
    "ENFJ": [
        {"name": "정치인", "description": "국민을 대표하여 정책을 수립하고 사회 변화를 이끌어가는 직업."},
        {"name": "교육자", "description": "학생들을 가르치고 지도하며 지식과 인성을 함양시키는 데 기여하는 전문가."},
        {"name": "조직 개발 컨설턴트", "description": "기업이나 조직의 성과 향상을 위해 조직 문화 및 역량 개발을 돕는 전문가."}
    ],
    "ENTJ": [ # [【1】](https://www.jobkorea.co.kr/goodjob/tip/view?News_No=18406)
        {"name": "CEO (최고경영자)", "description": "기업의 전반적인 운영을 책임지고 전략적인 결정을 내리는 최고 리더."},
        {"name": "투자 은행가", "description": "기업 인수합병, 자금 조달 등을 자문하고 투자 전략을 수립하는 금융 전문가."},
        {"name": "관리자", "description": "조직이나 팀의 목표 달성을 위해 자원을 효율적으로 배분하고 지휘하는 직업."}
    ]
}

# --- 웹 앱 UI 구성 시작 ---

st.title("💖 나의 MBTI와 어울리는 직업 찾기 💖")
st.markdown("---") # 무채색 배경에 잘 어울리는 구분선

st.write("안녕 누나! 초등학교 교사를 꿈꾸는 누나를 위한 진로 탐색 도우미예요!")
st.write("자신의 MBTI 유형을 선택하면, 그 유형에 어울리는 직업들을 추천해 줄게!")

# MBTI 유형 선택 (정렬된 목록으로)
# 첫 번째 옵션은 빈 문자열로 두어 사용자에게 선택을 유도
mbti_types_sorted = sorted(mbti_jobs_with_descriptions.keys())
selected_mbti = st.selectbox(
    "✨ 당신의 MBTI 유형을 선택해보세요!",
    ["-- MBTI를 선택해주세요 --"] + mbti_types_sorted, # 첫 번째 옵션 추가
    index=0 # 첫 번째 옵션을 기본으로 선택
)

# MBTI가 선택되었을 때만 직업 추천 보여주기
if selected_mbti != "-- MBTI를 선택해주세요 --":
    st.markdown(f"### 💡 당신은 <span style='color:#FF6347;'>`{selected_mbti}`</span>! 이 유형에 어울리는 직업을 추천해요.", unsafe_allow_html=True) # 포인트 컬러 (주황색 계열) 적용

    recommended_jobs = mbti_jobs_with_descriptions.get(selected_mbti, [])

    if recommended_jobs:
        for job_info in recommended_jobs:
            st.markdown(f"- **{job_info['name']}**: {job_info['description']}") # 직업 이름 강조
            # st.markdown(f"") # 줄 바꿈
    else:
        st.write("아직 준비된 직업 추천이 없어요! 😢")

    st.success("이 추천들이 누나의 진로 탐색에 도움이 되기를 바라요! 😊")
