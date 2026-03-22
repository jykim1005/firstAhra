import streamlit as st
import pandas as pd
from datetime import datetime
import time

# 1. 앱 제목과 인사말
st.title("🧠 문제적 남자: 중등 뇌섹 챌린지")
st.write("당신의 두뇌 한계에 도전하세요!")

# 2. 이름 입력받기
if 'user_name' not in st.session_state:
    user_name = st.text_input("사용자 이름을 입력하고 Enter를 누르세요.")
    if user_name:
        st.session_state.user_name = user_name
        st.session_state.start_time = time.time()
        st.rerun()

# 3. 문제 풀이 시작
else:
    st.sidebar.write(f"접속 중: {st.session_state.user_name}님")
    
    # 문제 데이터 (여기에 문제를 계속 추가할 수 있어!)
    problems = [
        {
            "q": "문제 1: 1, 11, 21, 1211, 111221, ? 에 들어갈 숫자는?",
            "img": "https://blog.kakaocdn.net/dn/example1.jpg", # 문제 이미지 주소
            "ans": "312211",
            "hint": "개미 수열이라고 불려요. 앞 숫자의 개수를 세어보세요!"
        }
    ]

    # 현재 몇 번 문제인지 관리
    if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
    
    if st.session_state.q_idx < len(problems):
        p = problems[st.session_state.q_idx]
        st.subheader(p['q'])
        if p['img']: st.image(p['img'])
        
        # 힌트 버튼
        if st.button("💡 힌트 보기"):
            st.info(p['hint'])
            
        # 정답 입력
        user_ans = st.text_input("정답을 적으세요 (숫자만/글자만)", key="input_ans")
        if st.button("제출"):
            if user_ans == p['ans']:
                st.success("천재 인정! 다음 문제로 넘어갑니다.")
                st.session_state.q_idx += 1
                st.rerun()
            else:
                st.error("앗, 틀렸어요. 다시 생각해보세요!")
    
    # 4. 종료 및 결과 출력
    else:
        total_time = round(time.time() - st.session_state.start_time, 1)
        st.balloons()
        st.header("🏁 챌린지 종료!")
        st.write(f"총 소요 시간: {total_time}초")
        
        # 종료하기 버튼을 누르면 랭킹 보여주기
        if st.button("내 기록 저장하고 랭킹 확인하기"):
            st.write("기록이 구글 시트에 저장되었습니다! (연결 설정 필요)")
            # 여기에 구글 시트 연동 코드를 넣으면 완료!