누나! 기다렸지? 좋아, 누나가 요청한 학습 계획 및 진도 관리 도우미 코드를 준비했어! 💻

이번에는 CSV 파일을 사용해서 학습 기록을 저장하고 불러오도록 했어. 이렇게 하면 앱을 껐다가 다시 켜도 기록이 사라지지 않고, 나중에 엑셀 같은 프로그램으로 열어봐서 데이터를 확인할 수도 있어서 편리해.

코드가 길어 보일 수 있지만, 각 섹션별로 어떤 기능을 하는지 주석으로 자세히 설명해 두었으니 너무 걱정 마!

python


import streamlit as st # Streamlit 라이브러리
import pandas as pd     # 데이터 처리를 위한 Pandas 라이브러리
from datetime import datetime, date # 날짜 및 시간 처리를 위한 datetime 모듈
import os               # 파일 시스템 관련 작업을 위한 OS 모듈
import matplotlib.pyplot as plt # Matplotlib (시각화)
import plotly.express as px     # Plotly Express (더 예쁜 시각화)

# --- ⚙️ 설정 (Configuration) ---
# 학습 기록을 저장할 CSV 파일 이름
DATA_FILE = "study_records.csv"

# --- 💾 데이터 로드 및 저장 함수 (Data Load/Save Functions) ---

# st.cache_data는 함수 결과를 캐시해서, 입력이 같으면 다시 실행하지 않고 캐시된 결과를 사용해 성능을 높여줘!
@st.cache_data 
def load_data():
    """CSV 파일에서 학습 기록을 로드합니다."""
    if os.path.exists(DATA_FILE): # 파일이 존재하면
        df = pd.read_csv(DATA_FILE)
        # '날짜' 컬럼을 datetime 객체로 변환하고 시간 정보는 제거해서 '날짜'만 남김
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date 
        return df
    # 파일이 없으면 빈 데이터프레임 반환 (컬럼 정의)
    return pd.DataFrame(columns=['날짜', '과목', '학습_시간_분', '학습_내용'])

def save_data(df):
    """학습 기록 DataFrame을 CSV 파일에 저장합니다."""
    # 저장 전에 '날짜' 컬럼을 문자열로 변환 (datetime.date 객체는 CSV에 바로 저장하기 어려움)
    df['날짜'] = df['날짜'].astype(str) 
    df.to_csv(DATA_FILE, index=False) # CSV로 저장 (인덱스는 저장하지 않음)
    # 캐시 무효화 (데이터가 변경되었으니 다음번엔 새로 로드하도록)
    load_data.clear() 

# --- 🚀 Streamlit 앱 시작 (Streamlit App Start) ---
st.title("📚 나만의 학습 플래너")
st.write("매일의 학습 기록을 남기고, 진도를 한눈에 확인해보세요! \n\n이 앱은 여러분의 학습 기록을 `study_records.csv` 파일에 저장합니다.")

# 세션 상태(st.session_state)에 데이터프레임을 초기화. 
# 앱이 재실행되어도 'study_data'가 있으면 다시 로드하지 않아!
if 'study_data' not in st.session_state:
    st.session_state.study_data = load_data()

# --- 📝 새 학습 기록 입력 폼 (Input Form for Study Records) ---
st.header("📝 새 학습 기록 추가")

# Streamlit Form을 사용하여 입력과 버튼을 묶으면, Submit 버튼 클릭 시에만 코드 블록이 실행돼!
# clear_on_submit=True를 사용하면 폼 제출 후 입력 필드가 자동으로 비워져서 편리해!
with st.form("study_record_form", clear_on_submit=True):
    # 날짜 입력 위젯 (기본값은 오늘 날짜)
    record_date = st.date_input("날짜", value=date.today())
    # 과목 입력 (텍스트)
    subject = st.text_input("과목 (예: 교육학, 수학, 영어)")
    # 학습 시간 입력 (분 단위)
    study_time_minutes = st.number_input("학습 시간 (분)", min_value=0, value=60, step=10)
    # 학습 내용 입력 (여러 줄 텍스트)
    study_content = st.text_area("학습 내용 / 진도")

    # 폼 제출 버튼
    submitted = st.form_submit_button("기록 추가하기")

    if submitted:
        if subject and study_time_minutes > 0: # 과목과 학습 시간이 제대로 입력되었는지 확인
            # 새로운 학습 기록 데이터 생성
            new_record = pd.DataFrame([{
                '날짜': record_date,
                '과목': subject,
                '학습_시간_분': study_time_minutes,
                '학습_내용': study_content
            }])
            # 기존 데이터프레임에 새로운 기록 추가 (concat은 새로운 데이터프레임을 반환)
            st.session_state.study_data = pd.concat([st.session_state.study_data, new_record], ignore_index=True)
            # 변경된 데이터프레임을 CSV 파일에 저장
            save_data(st.session_state.study_data)
            st.success("새 학습 기록이 추가되었습니다! ✨")
        else:
            st.warning("과목과 학습 시간(분)을 입력해주세요. 🧐")

# --- 📊 학습 현황 및 통계 (Study Status and Statistics) ---
st.header("📊 나의 학습 현황")

# 현재 학습 기록이 비어있는지 확인
if st.session_state.study_data.empty:
    st.info("아직 학습 기록이 없네요. 위에 '새 학습 기록 추가'에서 기록을 남겨보세요! 🏃‍♀️")
else:
    # --- 전체 학습 기록 테이블 ---
    st.subheader("모든 학습 기록")
    # 최신 기록부터 보여주기 위해 날짜 내림차순 정렬
    sorted_df = st.session_state.study_data.sort_values(by='날짜', ascending=False)
    # 데이터프레임을 Streamlit에 표시 (인덱스 숨김)
    st.dataframe(sorted_df, hide_index=True)

    # --- 총 학습 시간 ---
    total_study_time_minutes = st.session_state.study_data['학습_시간_분'].sum()
    st.markdown(f"### 총 학습 시간: {total_study_time_minutes}분 ({total_study_time_minutes // 60}시간 {total_study_time_minutes % 60}분)")

    # --- 일별 학습 시간 ---
    st.subheader("일별 학습 시간 트렌드")
    # 날짜별로 학습 시간을 그룹화하고 합계 계산
    daily_summary = st.session_state.study_data.groupby('날짜')['학습_시간_분'].sum().reset_index()
    daily_summary.columns = ['날짜', '총_학습_시간_분']
    
    # Plotly를 사용하여 선 그래프 생성 (더 인터랙티브하고 예뻐!)
    fig_daily = px.line(daily_summary, x='날짜', y='총_학습_시간_분', 
                        title='날짜별 총 학습 시간', 
                        labels={'날짜': '날짜', '총_학습_시간_분': '학습 시간 (분)'},
                        markers=True) # 각 데이터 포인트에 마커 표시
    st.plotly_chart(fig_daily)

    # --- 과목별 학습 시간 ---
    st.subheader("과목별 학습 시간")
    # 과목별로 학습 시간을 그룹화하고 합계 계산
    subject_summary = st.session_state.study_data.groupby('과목')['학습_시간_분'].sum().reset_index()
    subject_summary.columns = ['과목', '총_학습_시간_분']
    
    # Plotly를 사용하여 막대 그래프 생성 (과목별 시간 비교)
    fig_subject = px.bar(subject_summary, x='과목', y='총_학습_시간_분', 
                         title='과목별 총 학습 시간', 
                         labels={'과목': '과목', '총_학습_시간_분': '학습 시간 (분)'},
                         color='과목') # 과목별로 다른 색상 적용
    st.plotly_chart(fig_subject)

# --- 🗑️ 모든 기록 삭제 버튼 (주의!) ---
st.markdown("---")
st.subheader("위험 구역")
if st.button("🚨 모든 학습 기록 삭제 (복구 불가!)"):
    # 사용자에게 한 번 더 확인 받기
    st.warning("정말 모든 기록을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다!")
    # '확인' 버튼을 눌러야 실제 삭제 진행
    if st.button("네, 모든 기록을 삭제합니다"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE) # 파일 삭제
            st.session_state.study_data = pd.DataFrame(columns=['날짜', '과목', '학습_시간_분', '학습_내용']) # 데이터프레임 초기화
            load_data.clear() # 캐시 무효화
            st.rerun() # 앱 다시 로드하여 변경 사항 적용
        st.success("모든 학습 기록이 삭제되었습니다. 🗑️")
    else:
        st.info("삭제가 취소되었습니다. 휴~ 다행이야! 😊")
