import streamlit as st
import json
import random
import os
import time

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Sheep Study", page_icon="✿", layout="wide")
CORAL_PINK = "#ff6b86"

# --- 2. CSS FIX TRÀN KHUNG & TIÊU ĐỀ ---
st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stHeader"] {{display: none;}}

    .stApp {{
        background-image: url("https://png.pngtree.com/background/20250606/original/pngtree-back-to-school-artistic-background-picture-image_16624609.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        background: rgba(255, 255, 255, 0.92); 
        border-radius: 25px;
        padding: 2rem 3rem !important;
        margin-top: 1rem !important;
        max-width: 900px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }}

    .main-title {{
        text-align: center;
        color: {CORAL_PINK};
        font-size: clamp(35px, 7vw, 65px) !important;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}

    .stButton > button {{
        width: 100% !important;
        min-height: 60px !important;
        border-radius: 15px !important;
        background-color: {CORAL_PINK} !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: none !important;
    }}

    .timer-box {{
        padding: 10px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        background: white;
        border: 2px solid {CORAL_PINK};
        margin-bottom: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC HỆ THỐNG ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'temp_choice' not in st.session_state: st.session_state.temp_choice = None
if 'answered' not in st.session_state: st.session_state.answered = False
if 'start_time' not in st.session_state: st.session_state.start_time = None

def load_data(grade, subject, mode):
    fname = f"data/{subject}/{grade}_{mode}.json"
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# --- 4. CÁC TRANG ---
if st.session_state.page == 'welcome':
    st.markdown('<p class="main-title">✿ SHEEP STUDY ✿</p>', unsafe_allow_html=True)
    st.write("<p style='text-align: center; font-size: 20px; font-weight:500;'>Học tập thông minh cùng Cừu nhỏ!</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1]) 
    with col2:
        if st.button("BẮT ĐẦU HỌC"):
            st.session_state.page = 'select'
            st.rerun()

elif st.session_state.page == 'select':
    st.markdown(f"<h2 style='color: {CORAL_PINK}; text-align: center;'>LỰA CHỌN MÔN HỌC</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        sb_name = st.selectbox("Môn học", ["Toán", "KHTN"])
        subject = "toan" if sb_name == "Toán" else "khtn"
    with c2:
        grade = st.selectbox("Lớp", ["6", "7", "8", "9"])
    
    mode_name = st.radio("Chế độ", ["Trắc nghiệm", "Kiểm tra", "Lý thuyết"], horizontal=True)
    mode = "theory" if mode_name == "Lý thuyết" else "quiz" if mode_name == "Trắc nghiệm" else "test"
    
    res = load_data(grade, subject, mode)
    selected_chapter = "Tất cả"
    if res and mode != 'theory':
        chapters = sorted(list(set([q.get('chapter', 'Khác') for q in res])))
        chapters.insert(0, "Tất cả")
        selected_chapter = st.selectbox("Chọn Chương:", chapters)

    if st.button("VÀO HỌC"):
        if res:
            if mode != 'theory':
                st.session_state.data = [q for q in res if q.get('chapter') == selected_chapter] if selected_chapter != "Tất cả" else res
                random.shuffle(st.session_state.data)
            else:
                st.session_state.data = res
            st.session_state.mode, st.session_state.page = mode, 'doing'
            st.session_state.current_idx, st.session_state.score = 0, 0
            st.session_state.temp_choice, st.session_state.answered = None, False
            st.session_state.start_time = time.time()
            st.rerun()
        else: st.error("⚠️ Không có dữ liệu!")

elif st.session_state.page == 'doing':
    if st.button("⬅ QUAY LẠI"):
        st.session_state.page = 'select'
        st.rerun()
        
    data = st.session_state.data
    if st.session_state.mode == 'test':
        rem = max(0, 600 - int(time.time() - st.session_state.start_time))
        m, s = divmod(rem, 60)
        st.markdown(f'<div class="timer-box">⏱️ {m:02d}:{s:02d}</div>', unsafe_allow_html=True)
        if rem <= 0: st.session_state.current_idx = 999; st.rerun()

    idx = st.session_state.current_idx
    total_q = min(len(data), 20)
    
    if idx < total_q:
        st.write(f"📝 **Câu {idx + 1} / {total_q}**")
        st.progress((idx + 1) / total_q)
        q = data[idx]
        st.info(q.get('question'))
        
        cols = st.columns(2)
        for i, opt in enumerate(q.get('options', [])):
            with cols[i % 2]:
                if st.button(opt, key=f"o_{idx}_{i}", disabled=st.session_state.answered, 
                             type="primary" if st.session_state.temp_choice == i else "secondary"):
                    st.session_state.temp_choice = i
                    st.rerun()

        st.markdown("---")
        # NẾU CHƯA TRẢ LỜI -> HIỆN NÚT XÁC NHẬN
        if not st.session_state.answered:
            if st.session_state.temp_choice is not None:
                if st.button("✅ XÁC NHẬN"):
                    st.session_state.answered = True
                    if st.session_state.temp_choice == q.get('answer'):
                        st.session_state.score += 1
                    st.rerun()
        # NẾU ĐÃ TRẢ LỜI -> HIỆN KẾT QUẢ & NÚT TIẾP THEO
        else:
            if st.session_state.temp_choice == q.get('answer'):
                st.success("Chính xác! ✨")
            else:
                st.error(f"Sai rồi! Đáp án đúng: {q['options'][q['answer']]}")
            
            if st.button("CÂU TIẾP THEO ➡"):
                st.session_state.current_idx += 1
                st.session_state.temp_choice = None
                st.session_state.answered = False
                st.rerun()
    else:
        st.balloons()
        st.success(f"🏆 Điểm của bạn: {st.session_state.score}/{total_q}")
        if st.button("LÀM LẠI"):
            st.session_state.page = 'select'
            st.rerun()
