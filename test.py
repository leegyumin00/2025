import streamlit as st # Streamlit 라이브러리를 가져와
import random          # 랜덤으로 숫자를 뽑기 위한 라이브러리

# --- ✨ 오늘의 한 줄 명언/문장 리스트 ---
# 여기 있는 문장들 중에서 랜덤으로 하나를 보여줄 거야.
# 누나가 좋아하는 문장이나 명언으로 자유롭게 바꿔 넣어도 돼!
quotes = [
    "배움은 그 자체로 가장 큰 보상이다.",
    "교육의 목적은 백지 위에 그림을 그리는 것이 아니라, 이미 그려진 그림을 밝히는 것이다. - 로버트 프로스트",
    "가장 강력한 무기는 교육이다. - 넬슨 만델라",
    "독서는 앉아서 하는 여행이다. - 오웰린",
    "시작이 반이다. 지금 바로 시작해봐!",
    "어제의 나와 오늘의 나는 다르다. 매일 성장하고 있어!",
    "강물은 흐르는 것을 멈추지 않는다. 너의 노력도 멈추지 마라.",
    "생각하는 대로 살지 않으면, 사는 대로 생각하게 된다. - 파스칼",
    "가르치는 일은 두 번 배우는 것이다. - 주세페 마치니",
    "인생은 용감한 모험이거나 아무것도 아니다. - 헬렌 켈러",
    "긍정적인 생각은 긍정적인 삶을 만든다."
]

# --- 🚀 웹 앱 제목 설정 ---
st.title("✨ 오늘의 한 줄 ✨")
st.write("마음을 다독이고 영감을 주는 한 문장을 만나보세요.")

# --- 🔄 세션 상태 초기화 (제일 중요한 부분이야!) ---
# 'session_state'는 Streamlit 앱이 새로고침될 때도 변수 값을 기억하게 해주는 기능이야.
# 그래서 버튼을 누르기 전까지는 같은 명언이 유지되다가, 버튼을 누르면 새로운 명언으로 바뀌는 거지!
if 'current_quote_index' not in st.session_state:
    # 앱을 처음 시작할 때만 랜덤으로 인덱스를 선택해서 저장해
    st.session_state.current_quote_index = random.randint(0, len(quotes) - 1)

# --- 💬 명언 표시 ---
# 세션 상태에 저장된 인덱스에 해당하는 명언을 가져와
current_quote = quotes[st.session_state.current_quote_index]

# `st.markdown`을 사용해서 글씨를 좀 더 크게 보여줄 수 있어!
st.markdown(f"## {current_quote}") 

st.markdown("---") # 구분선

# --- ▶️ 다음 문장 보기 버튼 ---
# 이 버튼을 누르면 새로운 문장이 나타나도록 할 거야.
if st.button("다음 문장 보기 👉"):
    # 버튼이 클릭되면 새로운 랜덤 인덱스를 생성해.
    new_index = random.randint(0, len(quotes) - 1)
    
    # 만약 같은 명언이 연속으로 나오는 걸 방지하고 싶다면 (선택 사항)
    # while new_index == st.session_state.current_quote_index:
    #     new_index = random.randint(0, len(quotes) - 1)
            
    # 새로운 인덱스를 세션 상태에 저장해 (이 부분이 바뀌면 앱이 다시 그려져)
    st.session_state.current_quote_index = new_index
    
    # Streamlit은 버튼이 클릭되면 스크립트 전체를 다시 실행하면서
    # 바뀐 session_state 값을 사용해서 화면을 새로 그려주기 때문에,
    # 별도로 `st.experimental_rerun()` 같은 걸 호출할 필요 없어!

# 앱 하단에 간단한 안내 메시지
st.caption("새로운 문장을 보려면 '다음 문장 보기' 버튼을 눌러보세요!")
