import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection

# --- 앱 설정 및 제목 ---
st.set_page_config(page_title="문제적 남자 챌린지")
st.title("🧠 문제적 남자: 30인분 뇌섹 퀴즈")

# --- 1. 전체 30문제 데이터 (예시 3개 + 나머지 빈칸) ---
# 중학생 개발자님, 여기에 문제를 30개까지 채워넣으세요!
if 'problems' not in st.session_state:
    st.session_state.problems = [
        {"q": "Q1. 1, 11, 21, 1211, 111221, ? (개미수열)", "ans": "312211", "desc": "숫자를 읽고 그 개수를 뒤에 붙이는 방식입니다. 1(1개) -> 11, 1(2개) -> 12..."},
        {"q": "Q2. 'TEN' + 'TEN' = ?", "ans": "20", "desc": "로마 숫자 X(10)와 X(10)를 더하면 20입니다."},
        {"q": "Q3. 낮에 동전을 찾은 이유는?", "ans": "낮이라서", "desc": "빛이 없어도 낮에는 해가 떠있기 때문에 동전이 잘 보입니다."},
        # ... 여기에 4번부터 30번까지 같은 형식으로 추가하세요!
    ]
    # 30개를 채우기 귀찮다면 아래 코드가 자동으로 가짜 문제를 만들어줍니다.
    for i in range(4, 31):
        st.session_state.problems.append({"q": f"Q{i}. 준비 중인 문제입니다.", "ans": "패스", "desc": "아직 설명이 등록되지 않았습니다."})

# --- 2. 상태 관리 초기화 ---
if 'user_name' not in st.session_state:
    name = st.text_input("사용자 이름을 입력하세요:")
    if st.button("시작하기"):
        st.session_state.user_name = name
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.show_desc = False # 설명 보기 상태
        st.session_state.start_time = time.time()
        st.rerun()

else:
    # 랭킹 등록 함수
    def save_ranking(final_score, elapsed_time):
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            existing_data = conn.read(worksheet="Ranking")
            new_record = pd.DataFrame([{
                "Name": st.session_state.user_name,
                "Score": final_score,
                "Time": elapsed_time,
                "Date": time.strftime("%Y-%m-%d %H:%M:%S")
            }])
            updated_df = pd.concat([existing_data, new_record], ignore_index=True)
            conn.update(worksheet="Ranking", data=updated_df)
            st.success("🏆 랭킹 등록 완료!")
        except:
            st.error("구글 시트 연결을 확인해주세요!")

    # --- 3. 문제 풀이 화면 ---
    problems = st.session_state.problems
    if st.session_state.q_idx < len(problems):
        curr_p = problems[st.session_state.q_idx]
        st.sidebar.write(f"현재 문제: {st.session_state.q_idx + 1} / 30")
        st.sidebar.write(f"맞힌 개수: {st.session_state.score}")
        
        st.subheader(curr_p['q'])
        
        # 정답 입력창
        user_ans = st.text_input("정답을 입력하세요:", key=f"input_{st.session_state.q_idx}")
        
        # 버튼들 배치
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("제출"):
                if user_ans == curr_p['ans']:
                    st.success("정답입니다!")
                    st.session_state.score += 1
                    st.session_state.show_desc = True # 정답 맞혀도 설명 보여주기
                else:
                    st.error("틀렸습니다!")

        with col2:
            if st.button("🏳️ 포기하기"):
                st.session_state.show_desc = True # 설명 보기 활성화
        
        with col3:
            if st.button("➡️ 다음문제"):
                st.session_state.q_idx += 1
                st.session_state.show_desc = False # 설명 가리기 초기화
                st.rerun()

        with col4:
            if st.button("🛑 그만하기"):
                st.session_state.q_idx = 999 # 종료 상태로 만들기
                st.rerun()

        # 포기하기나 정답 제출 후 설명 보여주기
        if st.session_state.show_desc:
            st.info(f"**정답:** {curr_p['ans']}\n\n**설명:** {curr_p['desc']}")

    # --- 4. 종료 화면 ---
    else:
        total_time = round(time.time() - st.session_state.start_time, 1)
        st.balloons()
        st.header("🏁 풀이가 종료되었습니다!")
        st.write(f"최종 성적: {st.session_state.score} 문제 성공")
        st.write(f"소요 시간: {total_time}초")
        
        if st.button("기록 저장하고 랭킹 등록"):
            save_ranking(st.session_state.score, total_time)
            
        if st.button("처음으로 돌아가기"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
