import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. 앱 설정 ---
st.set_page_config(page_title="뇌섹남: 중등 논리 챌린지", layout="centered")

# --- 2. 중학생 수준 논리/수학 30문제 ---
if 'problems' not in st.session_state:
    raw_probs = [
        {"q": "1번: 10미터 우물 밑 달팽이가 낮에 3m 올라가고 밤에 2m 내려간다. 탈출에 며칠 걸릴까?", "ans": "8", "desc": "7일째 7m 위치, 8일째 낮에 3m를 올라가면 바로 탈출 성공입니다!"},
        {"q": "2번: 3, 3, 3, 3 네 개의 3을 사칙연산하여 '7'을 만드세요. (성공 시 '성공' 입력)", "ans": "성공", "desc": "3 + 3 + (3 / 3) = 7 입니다."},
        {"q": "3번: 사과 3개에서 2개를 가져갔다면, 당신은 사과를 몇 개 가지고 있나요?", "ans": "2", "desc": "내가 가져간 2개가 내가 가진 사과입니다."},
        {"q": "4번: 6이 9가 되는 가장 빠른 방법은 무엇일까요?", "ans": "뒤집기", "desc": "숫자 6을 180도 뒤집으면 9가 됩니다."},
        {"q": "5번: 성냥개비로 만든 '6+4=4'에서 1개만 옮겨 식을 완성하세요. (성공 시 '성공' 입력)", "ans": "성공", "desc": "6의 왼쪽 위 성냥을 옮겨 0으로 만들면 0+4=4가 됩니다."},
        {"q": "6번: 1부터 100까지 숫자 중 '9'는 총 몇 번 나올까요?", "ans": "20", "desc": "일의 자리 10번, 십의 자리 10번 해서 총 20번입니다."},
        {"q": "7번: 'O T T F F S S E N ?' 빈칸에 들어갈 알파벳은?", "ans": "T", "desc": "One, Two, Three... Ten(10)의 첫 글자입니다."},
        {"q": "8번: 12시 15분, 시침과 분침 사이의 각도는 몇 도일까요?", "ans": "82.5", "desc": "분침이 15분 갈 때 시침도 7.5도 움직이기 때문입니다."},
        {"q": "9번: 형제 7명에게 각각 여동생이 1명씩 있다면, 이 집 자녀는 총 몇 명?", "ans": "8", "desc": "여동생 1명이 모든 오빠들의 여동생입니다."},
        {"q": "10번: 2등을 추월하면 나는 몇 등일까요?", "ans": "2", "desc": "2등 자리를 차지했으니 2등입니다."},
        {"q": "11번: 어떤 숫자에 0을 곱하면 0입니다. 그럼 어떤 숫자를 0으로 나누면?", "ans": "없음", "desc": "수학적으로 0으로 나누는 것은 정의되지 않습니다."},
        {"q": "12번: 철수는 4층까지 계단 60개를 올라갔습니다. 8층까지는 총 몇 개일까요?", "ans": "140", "desc": "1층->4층은 3구간(60개), 한 층당 20개이므로 1층->8층은 7구간(140개)입니다."},
        {"q": "13번: 세발자전거, 자동차, 곤충의 다리 개수를 모두 곱하면?", "ans": "72", "desc": "3(바퀴) * 4(바퀴) * 6(다리) = 72입니다."},
        {"q": "14번: 아버지는 45세, 아들은 15세입니다. 아버지 나이가 아들의 2배가 되는 건 몇 년 후?", "ans": "15", "desc": "15년 후 아버지는 60세, 아들은 30세가 됩니다."},
        {"q": "15번: 1, 2, 4, 7, 11, 16... 다음에 올 숫자는 무엇일까요?", "ans": "22", "desc": "차례대로 1, 2, 3, 4, 5...씩 늘어나는 규칙입니다."},
        {"q": "16번: 성냥개비 6개로 정삼각형 4개를 만드는 방법은?", "ans": "입체", "desc": "삼각뿔(정사면체)을 입체로 만들면 삼각형 4개가 나옵니다."},
        {"q": "17번: 한 면이 3cm인 정육면체의 모든 모서리 길이의 합은?", "ans": "36", "desc": "정육면체의 모서리는 총 12개입니다. 3 * 12 = 36."},
        {"q": "18번: '바가지'를 거꾸로 하면 '지가바'입니다. '해골'을 거꾸로 하면?", "ans": "물", "desc": "해골(바가지)을 뒤집으면 내용물(물)이 쏟아집니다 (넌센스 논리)."},
        {"q": "19번: 직선으로만 이루어진 알파벳 'A, E, F, H, I, K, L, M, N' 다음은?", "ans": "T", "desc": "곡선이 없는 직선 알파벳의 순서입니다."},
        {"q": "20번: 뒤집어도 모양이 똑같은 세 자리 숫자 중 가장 큰 수는?", "ans": "888", "desc": "808, 181 등 중 888이 가장 큽니다."},
        {"q": "21번: 주사위 마주 보는 두 면의 합은 항상 얼마일까요?", "ans": "7", "desc": "1-6, 2-5, 3-4가 마주 보며 합은 7입니다."},
        {"q": "22번: 9, 18, 27, 36... 이 수열의 각 자릿수를 더하면 항상 얼마일까요?", "ans": "9", "desc": "9의 배수 판정법의 원리입니다."},
        {"q": "23번: 어떤 숫자에서 1을 뺐더니 0이 되었습니다. 이 숫자를 로마자로 쓰면?", "ans": "I", "desc": "로마자 I(1)에서 1을 빼면 0이 됩니다."},
        {"q": "24번: 한 변이 4인 정사각형의 넓이와 둘레가 같습니다. 이 숫자는?", "ans": "4", "desc": "4*4=16(넓이), 4*4=16(둘레)로 같습니다."},
        {"q": "25번: 00:00부터 12:00까지 시침과 분침은 몇 번 겹칠까요?", "ans": "11", "desc": "매 시간 겹치지만 11시~1시 사이에는 12시에 한 번만 겹칩니다."},
        {"q": "26번: 1, 4, 9, 16, 25... 다음에 올 숫자는?", "ans": "36", "desc": "1, 2, 3, 4, 5의 제곱수 순서입니다."},
        {"q": "27번: 금메달 5점, 은메달 3점, 동메달 1점일 때, 금1 은2 동4의 점수는?", "ans": "15", "desc": "5 + 6 + 4 = 15점입니다."},
        {"q": "28번: 1, 3, 4, 7, 11, 18... 다음에 올 숫자는?", "ans": "29", "desc": "앞의 두 수를 더해 다음 수가 되는 피보나치 수열 방식입니다."},
        {"q": "29번: 정삼각형 한 내각의 크기는 몇 도일까요?", "ans": "60", "desc": "180도를 3으로 나누면 60도입니다."},
        {"q": "30번: 머리카락이 없는 사람이 가장 좋아하는 알파벳은?", "ans": "O", "desc": "머리가 0(오)링 되었다는 언어유희입니다."}
    ]
    random.shuffle(raw_probs)
    st.session_state.problems = raw_probs

# --- 3. 초기 화면 ---
if 'user_name' not in st.session_state:
    st.title("🧠 뇌섹남: 중등 논리 챌린지")
    st.write("진짜 실력을 보여주세요! 문제는 무작위로 나옵니다.")
    name = st.text_input("당신의 이름을 입력하세요:")
    if st.button("챌린지 시작하기 🚀"):
        if name:
            st.session_state.user_name = name
            st.session_state.q_idx = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.show_desc = False
            st.rerun()
        else:
            st.warning("이름을 입력해야 시작할 수 있어요!")

# --- 4. 문제 풀이 화면 ---
else:
    probs = st.session_state.problems
    if st.session_state.q_idx < len(probs):
        p = probs[st.session_state.q_idx]
        st.subheader(f"Q{st.session_state.q_idx + 1}. {p['q']}")
        st.progress((st.session_state.q_idx) / len(probs))
        
        user_ans = st.text_input("정답 입력 (숫자 또는 단어):", key=f"ans_{st.session_state.q_idx}")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("✅ 제출"):
                # 공백 제거 및 소문자 변환으로 비교 정확도 높임
                if user_ans.strip().replace(" ", "").lower() == p['ans'].strip().replace(" ", "").lower():
                    st.success("정답입니다!")
                    st.session_state.score += 1
                    st.session_state.show_desc = True
                else:
                    st.error("틀렸습니다! 다시 생각해보세요.")
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

    # --- 5. 결과 및 랭킹 저장 ---
    else:
        duration = round(time.time() - st.session_state.start_time, 1)
        st.balloons()
        st.header("🏁 모든 문제를 마쳤습니다!")
        st.write(f"### {st.session_state.user
