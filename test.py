import streamlit as st
import random

# 웹 페이지의 제목 설정
st.title("🔢 재미있는 구구단 퀴즈!")

# 세션 상태(Session State) 초기화
# Streamlit 앱은 사용자 액션(버튼 클릭, 입력 등)이 있을 때마다 처음부터 다시 실행돼.
# 그래서 변수들의 값을 유지하려면 'st.session_state'에 저장해야 해.
if 'score' not in st.session_state:
    st.session_state.score = 0  # 현재 맞힌 문제 수
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0  # 총 문제 수
if 'num1' not in st.session_state:
    # 첫 문제 출제 (2단부터 9단까지)
    st.session_state.num1 = random.randint(2, 9)
if 'num2' not in st.session_state:
    st.session_state.num2 = random.randint(2, 9)

# 현재 문제 표시
st.write(f"## {st.session_state.num1} X {st.session_state.num2} = ?")

# 사용자에게 정답을 입력받는 칸
# key는 Streamlit에서 같은 타입의 위젯이 여러 개 있을 때 구분하기 위해 사용해.
user_answer = st.text_input("정답을 입력해주세요:", key="answer_input")

# '정답 확인!' 버튼
if st.button("정답 확인!"):
    st.session_state.question_count += 1 # 문제 수 1 증가

    try:
        # 사용자가 입력한 값을 숫자로 변환
        if int(user_answer) == st.session_state.num1 * st.session_state.num2:
            st.success("정답입니다! 🎉 다음 문제도 풀어볼까?")
            st.session_state.score += 1 # 점수 1 증가
        else:
            st.error(f"아쉽지만 오답이에요. 정답은 {st.session_state.num1 * st.session_state.num2}입니다. 😢 다시 도전!")
    except ValueError: # 숫자가 아닌 다른 것을 입력했을 때
        st.warning("숫자를 입력해주세요! 다시 시도해봐.")
    
    # 정답 확인 후 새로운 문제 출제
    st.session_state.num1 = random.randint(2, 9)
    st.session_state.num2 = random.randint(2, 9)
    # 입력창을 비우기 위해, `answer_input`의 값을 빈 문자열로 설정 (이 부분은 다음 페이지 로딩 시 자동으로 적용될 거야)
    st.session_state.answer_input = "" 


# 현재 점수 표시
st.write(f"---") # 구분선
st.write(f"**현재 점수: {st.session_state.score} / {st.session_state.question_count} 문제**")

# 초기화 버튼
if st.button("퀴즈 초기화"):
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.num1 = random.randint(2, 9)
    st.session_state.num2 = random.randint(2, 9)
    st.experimental_rerun() # 앱을 처음부터 다시 실행 (필수 아님, 변화 바로 적용 위함)

