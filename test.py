import streamlit as st
import random

# 웹 페이지의 제목 설정
st.title("🔢 재미있는 구구단 퀴즈!")
st.write("2단부터 9단까지의 구구단 문제를 풀어보자! 🤔")

# 세션 상태(Session State) 초기화
# Streamlit 앱은 사용자 액션(버튼 클릭, 입력 등)이 있을 때마다 처음부터 다시 실행돼.
# 그래서 변수들의 값을 유지하려면 'st.session_state'에 저장해야 해.
if 'score' not in st.session_state:
    st.session_state.score = 0  # 현재 맞힌 문제 수
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0  # 총 문제 수
if 'num1' not in st.session_state:
    st.session_state.num1 = random.randint(2, 9) # 첫 번째 숫자 (단)
if 'num2' not in st.session_state:
    st.session_state.num2 = random.randint(2, 9) # 두 번째 숫자 (곱하는 수)
if 'message' not in st.session_state:
    st.session_state.message = "" # 사용자에게 보여줄 메시지

# 현재 문제 표시
st.write(f"### 문제: {st.session_state.num1} X {st.session_state.num2} = ?")

# Streamlit Form을 사용하여 입력과 버튼을 묶음
# Form을 사용하면 Submit 버튼 클릭 시에만 코드 블록이 실행되고 입력 필드가 자동으로 초기화돼!
with st.form("quiz_form", clear_on_submit=True):
    user_answer_str = st.text_input("정답을 입력해주세요:", key="answer_input_field")
    submit_button = st.form_submit_button("정답 확인!")

    # 폼이 제출되었을 때만 이 안의 로직이 실행돼.
    if submit_button:
        # 사용자가 정답 확인 버튼을 누르면 문제 수 증가
        st.session_state.question_count += 1
        
        try:
            user_answer = int(user_answer_str) # 사용자가 입력한 문자열을 숫자로 변환

            # 정답 확인 로직
            if user_answer == st.session_state.num1 * st.session_state.num2:
                st.session_state.message = "정답입니다! 🎉 다음 문제도 풀어볼까?"
                st.session_state.score += 1 # 점수 1 증가
            else:
                st.session_state.message = (
                    f"아쉽지만 오답이에요. 😥 정답은 {st.session_state.num1 * st.session_state.num2}입니다. 다시 도전!"
                )
        except ValueError: # 사용자가 숫자가 아닌 다른 것을 입력했을 때
            st.session_state.message = "💡 숫자를 입력해주세요! 다시 시도해봐."
        
        # 새로운 문제 출제 (폼 제출 후 새로운 문제로 업데이트)
        st.session_state.num1 = random.randint(2, 9)
        st.session_state.num2 = random.randint(2, 9)
        # 중요: `st.text_input`의 `key`를 그대로 두면, 폼 제출 시 자동으로 초기화돼!


# 사용자에게 결과 메시지 표시
if st.session_state.message:
    # 메시지에 따라 색깔을 다르게 보여줄 수도 있어!
    if "정답입니다!" in st.session_state.message:
        st.success(st.session_state.message)
    elif "오답이에요" in st.session_state.message:
        st.error(st.session_state.message)
    else: # 숫자가 아닌 경우 등 경고 메시지
        st.warning(st.session_state.message)

# 현재 점수 표시
st.markdown("---") # 구분선
st.write(f"**현재 점수: {st.session_state.score} / {st.session_state.question_count} 문제**")

# 초기화 버튼
if st.button("🔄 퀴즈 초기화"):
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.num1 = random.randint(2, 9)
    st.session_state.num2 = random.randint(2, 9)
    st.session_state.message = "" # 메시지도 초기화
    st.rerun() # 전체 앱을 다시 실행하여 초기 상태로 돌아감
