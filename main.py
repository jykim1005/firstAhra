import streamlit as st
import pandas as pd
import time
import random  # 👈 문제를 섞기 위해 필요한 도구예요!
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. 앱 설정 ---
st.set_page_config(page_title="무작위! 문제적 남자", layout="centered")

# --- 2. 퀴즈 데이터 설정 (진짜 30문제) ---
if 'problems' not in st.session_state:
    raw_probs = [
        # --- 기존 10문제 ---
        {"q": "1번: 1월은 31, 2월은 28... '몇 월'이 항상 28일일까요?", "ans": "모든달", "desc": "모든 달은 최소 28일 이상을 가지고 있어요!"},
        {"q": "2번: 1=5, 2=25, 3=125, 4=625 일 때, 5=?", "ans": "1", "desc": "첫 줄에서 1=5라고 했으니 5=1입니다."},
        {"q": "3번: 숫자 '8'을 세로로 반 나누면 어떤 숫자가 될까요?", "ans": "3", "desc": "8을 세로로 쪼개면 숫자 3 모양이 나옵니다."},
        {"q": "4번: 성냥개비 6개로 정삼각형 4개를 만드는 방법은?", "ans": "입체", "desc": "평면이 아닌 삼각뿔(입체)을 만들면 됩니다."},
        {"q": "5번: 세상에서 가장 시원한 알파벳 3개는?", "ans": "ACF", "desc": "에어컨(AC)과 선풍기(Fan)의 앞글자예요."},
        {"q": "6번: 8809에는 동그라미 구멍이 몇 개 있을까요?", "ans": "5", "desc": "8(2)+8(2)+0(1)+9(0) = 5개입니다."},
        {"q": "7번: 'S, M, T, W, T, F, ?' 빈칸에 들어갈 알파벳은?", "ans": "S", "desc": "요일(Sunday~Saturday)의 앞글자예요."},
        {"q": "8번: 부모님에겐 있고 자식에겐 없는 글자 받침은?", "ans": "받침", "desc": "부모님에는 받침이 있고 자식에는 없죠!"},
        {"q": "9번: '가나다라마바사'는 7글자입니다. '이것'은 몇 글자일까요?", "ans": "2", "desc": "'이것'이라는 단어는 2글자입니다."},
        {"q": "10번: 2등을 추월하면 나는 몇 등일까요?", "ans": "2", "desc": "2등 자리를 뺏었으니 내가 2등이 됩니다."},

        # --- 새로운 20문제 추가 ---
        {"q": "11번: 알파벳 A부터 Z까지 중 가장 시끄러운 알파벳은?", "ans": "G", "desc": "쥐(G) 잡는 소리가 시끄러워서 그렇다는 넌센스 퀴즈입니다."},
        {"q": "12번: 3, 3, 8, 8 네 숫자를 사칙연산해서 24를 만드세요. (답은 '성공' 입력)", "ans": "성공", "desc": "8 / (3 - 8/3) = 24 입니다. 아주 어려운 수학 문제죠!"},
        {"q": "13번: 목수가 '문'을 만들 때 가장 먼저 하는 일은?", "ans": "구멍", "desc": "문 고리나 경첩을 달기 위해 구멍을 먼저 뚫어야 하거나, 문틀을 짭니다."},
        {"q": "14번: '나'는 누구일까? 나는 물 속에서도 살고 땅 위에서도 살지만 발이 없어.", "ans": "그림자", "desc": "물 위에도 땅 위에도 비치지만 발이 없습니다."},
        {"q": "15번: 숫자 1부터 100까지 9는 모두 몇 번 나올까요?", "ans": "20", "desc": "9, 19... 89(9번) + 90, 91... 99(11번) = 총 20번입니다."},
        {"q": "16번: 시계가 1시에는 1번, 2시에는 2번 종이 울립니다. 3시에는 몇 초 동안 울릴까요?", "ans": "0", "desc": "종이 울리는 횟수와 시간(초)은 별개입니다. (넌센스)"},
        {"q": "17번: 머리카락이 없는 사람이 가장 좋아하는 알파벳은?", "ans": "O", "desc": "머리가 '오'링(0) 되었다는 말장난입니다."},
        {"q": "18번: 'O T T F F S S E N ?' 빈칸에 들어갈 알파벳은?", "ans": "T", "desc": "숫자 영어 발음(One, Two, Three... Ten)의 첫 글자입니다."},
        {"q": "19번: 세상에서 가장 큰 '코'는 무엇일까요?", "ans": "멕시코", "desc": "나라 이름 멕시코(코)입니다."},
        {"q": "20번: 뒤집어도 모양이 변하지 않는 숫자는?", "ans": "8", "desc": "808, 101 처럼 대칭인 숫자나 8 자체를 뒤집어도 비슷합니다."},
        {"q": "21번: 펭귄이 다니는 중학교의 이름은?", "ans": "냉방중", "desc": "추운 곳에 살아서 '냉방중'학교입니다."},
        {"q": "22번: 소가 네 마리 있으면?", "ans": "소포", "desc": "소(Cow)가 네 마리(Four)라서 소포입니다."},
        {"q": "23번: 차는 차인데 타지 못하는 차는?", "ans": "마시는차", "desc": "녹차, 홍차 같은 마시는 차입니다."},
        {"q": "24번: 도둑이 가장 좋아하는 아이스크림은?", "ans": "보석바", "desc": "반짝이는 보석을 좋아하니까요!"},
        {"q": "25번: 학생이 가장 좋아하는 산은?", "ans": "하산", "desc": "학교가 끝나는 하산입니다."},
        {"q": "26번: 수학책을 불에 태우면?", "ans": "수학익힘", "desc": "수학이 익어버려서 수학익힘책이 됩니다."},
        {"q": "27번: 아침에 다리 네 개, 점심에 두 개, 저녁에 세 개인 것은?", "ans": "사람", "desc": "아기(기어다님), 어른(직립), 노인(지팡이)을 뜻합니다."},
        {"q": "28번: 왼쪽으로는 가도 오른쪽으로는 못 가는 것은?", "ans": "글자", "desc": "우리는 글자를 왼쪽에서 오른쪽 방향으로만 씁니다."},
        {"q": "29번: 눈이 오면 보이는 '눈'은?", "ans": "스노우볼", "desc": "눈(Snow)을 뭉친 덩어리입니다."},
        {"q": "30번: 칠할수록 하얘지는 것은?", "ans": "칠판", "desc": "분필로 칠할수록 하얀 가루가 묻어납니다 (칠판 종류에 따라 다름)."}
    ]
    
    # 섞기
    random.shuffle(raw_probs)
    st.session_state.problems = raw_probs

# --- 3. 초기 화면 ---
if 'user_name' not in st.session_state:
    st.title("🧠 무작위 뇌섹 챌린지")
    name = st.text_input("당신의 이름을 입력하세요:")
    if st.button("시작하기 🚀"):
        if name:
            st.session_state.user_name = name
            st.session_state.q_idx = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.show_desc = False
            st.rerun()
        else:
            st.warning("이름을 입력해주세요!")

# --- 4. 문제 풀이 화면 ---
else:
    probs = st.session_state.problems
    if st.session_state.q_idx < len(probs):
        p = probs[st.session_state.q_idx]
        st.subheader(f"제 {st.session_state.q_idx + 1}문. {p['q']}")
        st.progress((st.session_state.q_idx) / len(probs))
        
        user_ans = st.text_input("정답 입력:", key=f"ans_{st.session_state.q_idx}")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("✅ 제출"):
                if user_ans.replace(" ", "") == p['ans'].replace(" ", ""):
                    st.success("정답!")
                    st.session_state.score += 1
                    st.session_state.show_desc = True
                else:
                    st.error("오답!")
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

    # --- 5. 결과 및 저장 ---
    else:
        duration = round(time.time() - st.session_state.start_time, 1)
        st.balloons()
        st.header("🏁 종료!")
        st.write(f"### {st.session_state.user_name}님: {st.session_state.score}점 / {duration}초")

        if st.button("🏆 랭킹 등록하기"):
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df = conn.read(worksheet="Ranking")
                new_row = pd.DataFrame([{
                    "Name": st.session_state.user_name,
                    "Score": st.session_state.score,
                    "Time": duration,
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                result_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Ranking", data=result_df)
                st.success("랭킹 저장 성공!")
            except Exception as e:
                st.error(f"저장 실패! 에러: {e}")

        if st.button("처음으로"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
