import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection  # 이 줄이 꼭 있어야 해요!

# --- 앱 제목 ---
st.title("🧠 문제적 남자: 챌린지 모드")

# --- 문제 데이터 (여기에 문제를 원하는 만큼 추가해!) ---
problems = [
    {
        "q": "문제 1: 1, 11, 21, 1211, 111221, ? 에 들어갈 숫자는?",
        "img": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcM6W5%2FbtqByS8zS8H%2F6kK6K6K6K6K6K6K6K6K6K6%2Fimg.jpg", 
        "ans": "312211",
        "hint": "숫자를 소리 내어 읽어보세요. (예: 1이 한 개 = 11)"
    },
    {
        "q": "문제 2: 'SEX' + 'TEN' = '17' 일 때, 'TEN' + 'TEN'은?",
        "img": None,
        "ans": "20",
        "hint": "로마 숫자(X, V, I 등)를 생각해보세요."
    },
    {
        "q": "문제 3: 가로등 밑에 동전이 떨어져 있다. 하지만 가로등은 꺼져 있고 달빛도 없다. 그런데 멀리서 오던 사람이 동전을 바로 찾아냈다. 어떻게 된 일일까?",
        "img": None,
        "ans": "낮이었기 때문에",
        "hint": "빛이 없어도 물체를 볼 수 있는 시간대를 생각해보세요."
    }
]

# --- 상태 관리 (이름, 문제 번호 등 저장) ---
if 'user_name' not in st.session_state:
    name = st.text_input("사용자 이름을 입력하세요:")
    if st.button("시작하기"):
        st.session_state.user_name = name
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.rerun()
else:
    # 모든 문제를 다 풀었는지 확인
    if st.session_state.q_idx < len(problems):
        p = problems[st.session_state.q_idx]
        
        st.subheader(f"Q{st.session_state.q_idx + 1}. {p['q']}")
        if p['img']:
            st.image(p['img'])
        
        if st.button("💡 힌트 보기"):
            st.info(p['hint'])
            
        user_ans = st.text_input("정답 입력:", key=f"ans_{st.session_state.q_idx}")
        
        if st.button("제출하기"):
            if user_ans.replace(" ", "") == p['ans']:
                st.success("정답입니다! 👏")
                st.session_state.score += 1
                st.session_state.q_idx += 1
                time.sleep(1) # 1초 쉬었다가
                st.rerun()    # 다음 문제로!
            else:
                st.error("틀렸습니다. 다시 생각해보세요!")
    
    # 마지막 결과 화면
    else:
        total_time = round(time.time() - st.session_state.start_time, 1)
        st.balloons()
        st.header("🏁 모든 문제를 완료했습니다!")
        st.write(f"최종 점수: {st.session_state.score} / {len(problems)}")
        st.write(f"총 소요 시간: {total_time}초")
        
        if st.button("다시 시작하기"):
            del st.session_state.user_name
            st.rerun()


# 기록 저장 로직
if st.button("내 기록 랭킹에 등록하기"):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        existing_data = conn.read(worksheet="Ranking")
        
        new_record = pd.DataFrame([{
            "Name": st.session_state.user_name,
            "Score": st.session_state.score,
            "Time": total_time,
            "Date": time.strftime("%Y-%m-%d %H:%M:%S")
        }])
        
        updated_df = pd.concat([existing_data, new_record], ignore_index=True)
        conn.update(worksheet="Ranking", data=updated_df)
        st.success("🏆 랭킹 등록 완료! 구글 시트를 확인해보세요.")
    except Exception as e:
        st.error(f"오류가 발생했어요: {e}")
