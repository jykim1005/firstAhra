import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 앱 설정 ---
st.set_page_config(page_title="문제적 남자: 중등 뇌섹 챌린지", layout="centered")

# --- 1. 문제 데이터셋 (30문제) ---
# 리스트 안에 문제를 계속 추가하면 됩니다.
if 'problems' not in st.session_state:
    st.session_state.problems = [
        {"q": "1번: 1월은 31, 2월은 28, 3월은 31... 그렇다면 '몇 월'이 항상 28일일까요?", "ans": "모든달", "desc": "모든 달(1월~12월)은 최소 28일 이상을 가지고 있습니다."},
        {"q": "2번: 1 = 5, 2 = 25, 3 = 125, 4 = 625 일 때, 5 = ?", "ans": "1", "desc": "문제의 시작에서 1=5라고 했으므로 5는 1입니다."},
        {"q": "3번: 숫자 '8'을 세로로 반 나누면 무엇이 될까요?", "ans": "3", "desc": "8의 왼쪽이나 오른쪽 반을 보면 숫자 3 모양이 나옵니다."},
        {"q": "4번: 성냥개비 6개로 정삼각형 4개를 만드는 방법은?", "ans": "입체", "desc": "평면이 아닌 입체도형(정사면체)을 만들면 됩니다."},
        {"q": "5번: 세상에서 가장 시원한 알파벳 3개는?", "ans": "ACF", "desc": "에어컨(AC)과 선풍기(Fan)의 F를 합친 말장난입니다."},
        {"q": "6번: 0은 1개, 8은 2개, 6은 1개입니다. 그렇다면 8809에는 동그라미가 몇 개?", "ans": "5", "desc": "숫자 모양에 포함된 동그라미 구멍의 개수입니다. 8(2)+8(2)+0(1)+9(0) = 5개입니다."},
        {"q": "7번: 'S, M, T, W, T, F, ?' 빈칸에 들어갈 알파벳은?", "ans": "S", "desc": "요일(Sunday~Saturday)의 앞글자입니다."},
        {"q": "8번: 부모님에게는 있고 자식에게는 없으며, 하늘에는 있고 땅에는 없는 것은?", "ans": "받침", "desc": "글자의 받침(ㅁ, ㄴ, ㄹ 등)을 말합니다."},
        {"q": "9번: '가나다라마바사'는 7글자입니다. 그렇다면 '이것'은 몇 글자일까요?", "ans": "2", "desc": "'이것'이라는 단어 자체는 2글자입니다."},
        {"q": "10번: A와 B가 경주를 하는데, A가 2등을 추월했습니다. A는 몇 등일까요?", "ans": "2", "desc": "2등을 제쳤으므로 이제 A가 2등이 됩니다."},
    ]
    # 30개를 채우기 위해 나머지 20개는 임시 문제로 자동 생성합니다.
    for i in range(11, 31):
        st.session_state.problems.append({
            "q": f"{i}번: 준비 중인 문제입니다. 정답은 '패스'입니다.", 
            "ans": "패스", 
            "desc": "아직 문제가 업데이트되지 않았습니다."
        })

# --- 2. 상태 관리 초기화 ---
if 'user_name' not in st.session_state:
    st.title("🧠 문제적 남자: 챌린지")
    name = st.text_input("당신의 이름을 입력하세요:")
    if st.button("챌린지 시작하기"):
        if name:
            st.session_state.user_name = name
            st.session_state.q_idx = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.show_desc = False
            st.rerun()
        else:
            st.warning("이름을 입력해야 시작할 수 있어요!")

else:
    # --- 3. 구글 시트 저장 함수 ---
    def save_to_gsheet(score, total_time):
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            existing_data = conn.read(worksheet="Ranking")
            new_record = pd.DataFrame([{
                "Name": st.session_state.user_name,
                "Score": score,
                "Time": total_time,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])
            updated_df = pd.concat([existing_data, new_record], ignore_index=True)
            conn.update(worksheet="Ranking", data=updated_df)
            return True
        except Exception as e:
            st.error(f"저장 실패: {e}")
            return False

    # --- 4. 문제 풀이 화면 ---
    problems = st.session_state.problems
    
    # 문제를 다 풀지 않았을 때
    if st.session_state.q_idx < len(problems):
        curr_p = problems[st.session_state.q_idx]
        
        st.subheader(f"Q{st.session_state.q_idx + 1}. {curr_p['q']}")
        st.progress((st.session_state.q_idx) / len(problems)) # 진행 바
        
        user_ans = st.text_input("정답 입력 (띄어쓰기 없이):", key=f"ans_{st.session_state.q_idx}")

        # 버튼 레이아웃
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ 제출"):
                # 공백 제거 후 비교
                if user_ans.replace(" ", "") == curr_p['ans'].replace(" ", ""):
                    st.success("정답입니다!")
                    st.session_state.score += 1
                    st.session_state.show_desc = True
                else:
                    st.error("틀렸습니다!")
        
        with col2:
            if st.button("🏳️ 포기"):
                st.session_state.show_desc = True
        
        with col3:
            if st.button("➡️ 다음"):
                st.session_state.q_idx += 1
                st.session_state.show_desc = False
                st.rerun()
                
        with col4:
            if st.button("🛑 그만"):
                st.session_state.q_idx = 999 # 종료 상태로 강제 전환
                st.rerun()

        # 설명창 출력
        if st.session_state.show_desc:
            st.info(f"**정답:** {curr_p['ans']} \n\n **설명:** {curr_p['desc']}")

    # --- 5. 최종 결과 및 랭킹 등록 ---
    else:
        total_time = round(time.time() - st.session_state.start_time, 1)
        st.balloons()
        st.header("🏁 모든 문제 풀이 완료!")
        st.write(f"### {st.session_state.user_name}님의 성적")
        st.write(f"- 맞힌 문제: {st.session_state.score} / {len(problems)}")
        st.write(f"- 총 소요 시간: {total_time}초")
        
        if st.button("🏆 기록 저장 및 랭킹 등록하기"):
            if save_to_gsheet(st.session_state.score, total_time):
                st.success("랭킹 서버에 기록이 저장되었습니다!")
        
        if st.button("처음으로 돌아가기"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
