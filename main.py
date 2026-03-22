import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. 앱 기본 설정 ---
st.set_page_config(page_title="문제적 남자: 뇌섹 챌린지", layout="centered")

# --- 2. 퀴즈 문제 데이터 (30문제) ---
if 'problems' not in st.session_state:
    st.session_state.problems = [
        {"q": "1번: 1월은 31, 2월은 28... 그렇다면 '몇 월'이 항상 28일일까요?", "ans": "모든달", "desc": "모든 달은 최소 28일 이상을 가지고 있어요!"},
        {"q": "2번: 1=5, 2=25, 3=125, 4=625 일 때, 5=?", "ans": "1", "desc": "첫 문장에서 1=5라고 했으니 5=1입니다."},
        {"q": "3번: 숫자 '8'을 세로로 반 나누면 어떤 숫자가 될까요?", "ans": "3", "desc": "8을 세로로 쪼개면 숫자 3 모양이 나옵니다."},
        {"q": "4번: 성냥개비 6개로 정삼각형 4개를 만드는 방법은?", "ans": "입체", "desc": "평면이 아닌 삼각뿔(입체)을 만들면 됩니다."},
        {"q": "5번: 세상에서 가장 시원한 알파벳 3개는?", "ans": "ACF", "desc": "에어컨(AC)과 선풍기(Fan)의 앞글자예요."},
        {"q": "6번: 8809에는 동그라미 구멍이 몇 개 있을까요?", "ans": "5", "desc": "8(2개)+8(2개)+0(1개)+9(0개) = 5개입니다."},
        {"q": "7번: 'S, M, T, W, T, F, ?' 빈칸에 들어갈 알파벳은?", "ans": "S", "desc": "일요일부터 토요일(Saturday)까지의 앞글자예요."},
        {"q": "8번: 부모님에겐 있고 자식에겐 없는 글자 받침은?", "ans": "받침", "desc": "부모님 글자에는 받침이 있고 자식에는 없죠!"},
        {"q": "9번: '가나다라마바사'는 7글자입니다. '이것'은 몇 글자일까요?", "ans": "2", "desc": "'이것'이라는 단어는 2글자입니다."},
        {"q": "10번: 2등을 추월하면 나는 몇 등일까요?", "ans": "2", "desc": "2등 자리를 뺏었으니 내가 2등이 됩니다."}
    ]
    # 나머지 30번까지 가짜 문제 채우기
    for i in range(11, 31):
        st.session_state.problems.append({"q": f"{i}번 문제: 정답은 '패스'입니다.", "ans": "패스", "desc": "준비 중입니다."})

# --- 3. 초기 화면 (이름 입력) ---
if 'user_name' not in st.session_state:
    st.title("🧠 문제적 남자: 중등 뇌섹 챌린지")
    name = st.text_input("당신의 멋진 이름을 알려주세요:")
    if st.button("챌린지 시작하기 🚀"):
        if name:
            st.session_state.user_name = name
            st.session_state.q_idx = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.show_desc = False
            st.rerun()
        else:
            st.warning("이름을 꼭 입력해주세요!")

# --- 4. 문제 풀이 화면 ---
else:
    problems = st.session_state.problems
    
    if st.session_state.q_idx < len(problems):
        p = problems[st.session_state.q_idx]
        st.subheader(f"Q{st.session_state.q_idx + 1}. {p['q']}")
        
        # 진행률 표시
        st.progress((st.session_state.q_idx) / len(problems))
        
        user_ans = st.text_input("정답을 입력하세요 (띄어쓰기 없이):", key=f"input_{st.session_state.q_idx}")

        # 버튼들
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("✅ 제출"):
                if user_ans.replace(" ", "") == p['ans'].replace(" ", ""):
                    st.success("정답입니다!")
                    st.session_state.score += 1
                    st.session_state.show_desc = True
                else:
                    st.error("틀렸어요!")
        with c2:
            if st.button("🏳️ 포기"):
                st.session_state.show_desc = True
        with c3:
            if st.button("➡️ 다음"):
                st.session_state.q_idx += 1
                st.session_state.show_desc = False
                st.rerun()
        with c4:
            if st.button("🛑 그만"):
                st.session_state.q_idx = 999
                st.rerun()

        if st.session_state.show_desc:
            st.info(f"**정답:** {p['ans']}\n\n**설명:** {p['desc']}")

    # --- 5. 최종 결과 및 저장 ---
    else:
        total_time = round(time.time() - st.session_state.start_time, 1)
        st.balloons()
        st.header("🏁 챌린지 종료!")
        st.write(f"### {st.session_state.user_name}님의 점수: {st.session_state.score}점")
        st.write(f"걸린 시간: {total_time}초")

        if st.button("🏆 내 기록 랭킹에 등록하기"):
            try:
                # 구글 시트 연결
                conn = st.connection("gsheets", type=GSheetsConnection)
                
                # 기존 데이터 읽기
                try:
                    df = conn.read(worksheet="Ranking")
                except:
                    df = pd.DataFrame(columns=["Name", "Score", "Time", "Date"])
                
                # 새 기록 추가
                new_data = pd.DataFrame([{
                    "Name": st.session_state.user_name,
                    "Score": st.session_state.score,
                    "Time": total_time,
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(worksheet="Ranking", data=updated_df)
                st.success("랭킹 등록 완료! 친구들에게 자랑하세요!")
            except Exception as e:
                st.error("저장에 실패했어요. 구글 시트 권한(편집자)을 확인해주세요!")

        if st.button("처음으로 돌아가기"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
