import streamlit as st
import json
import random
import os

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Sheep Study", page_icon="✿", layout="wide")

CORAL_PINK = "#ff6b86"

# CSS làm giao diện xịn xò
st.markdown(f"""
    <style>
    .stButton>button {{
        width: 100%; border-radius: 20px; height: 3.5em;
        background-color: {CORAL_PINK}; color: white;
        font-weight: bold; font-size: 18px;
    }}
    .main-title {{
        text-align: center; color: {CORAL_PINK};
        font-size: 50px; font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# Khởi tạo trạng thái
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0

def load_data(grade, subject, mode):
    # Đường dẫn chuẩn theo cấu trúc của bạn: data/toan/6_quiz.json
    fname = f"data/{subject}/{grade}_{mode}.json"
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# --- TRANG CHÀO MỪNG ---
if st.session_state.page == 'welcome':
    st.markdown('<p class="main-title">✿ SHEEP STUDY ✿</p>', unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Hệ thống ôn tập thông minh</p>", unsafe_allow_html=True)
    if st.button("BẮT ĐẦU HỌC ♡"):
        st.session_state.page = 'select'
        st.rerun()

# --- TRANG CHỌN CHẾ ĐỘ ---
elif st.session_state.page == 'select':
    st.markdown(f"<h2 style='color: {CORAL_PINK};'>THIẾT LẬP ÔN TẬP</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        sb_name = st.selectbox("Chọn môn học", ["Toán", "KHTN"])
        subject = "toan" if sb_name == "Toán" else "khtn"
    with col2:
        grade = st.selectbox("Chọn lớp", ["6", "7", "8", "9"])
    
    mode_name = st.radio("Chế độ", ["Luyện tập (Quiz)", "Kiểm tra (Test)", "Lý thuyết (Theory)"], horizontal=True)
    mode = "quiz" if "Quiz" in mode_name else "test" if "Test" in mode_name else "theory"
    
    if st.button("VÀO HỌC NGAY"):
        res = load_data(grade, subject, mode)
        if res:
            st.session_state.data = res
            st.session_state.mode = mode
            if mode != 'theory': random.shuffle(st.session_state.data)
            st.session_state.page = 'doing'
            st.session_state.current_idx = 0
            st.session_state.score = 0
            st.rerun()
        else:
            st.error(f"Lỗi: Không tìm thấy file data/{subject}/{grade}_{mode}.json")

# --- TRANG HIỂN THỊ NỘI DUNG ---
elif st.session_state.page == 'doing':
    data = st.session_state.data
    
    # 1. NẾU LÀ LÝ THUYẾT (HIỂN THỊ DẠNG SƠ ĐỒ THẺ)
    if st.session_state.mode == 'theory':
        st.markdown(f"<h2 style='color: {CORAL_PINK};'>📖 LÝ THUYẾT TRỌNG TÂM</h2>", unsafe_allow_html=True)
        if st.button("← QUAY LẠI"):
            st.session_state.page = 'select'
            st.rerun()
            
        for chapter in data:
            with st.expander(f"📂 {chapter.get('title', 'Chương')}", expanded=True):
                for lesson in chapter.get('lessons', []):
                    st.success(f"🌿 {lesson['name']}")
                    # Tách nội dung thành các ý nhỏ để nhìn cho giống sơ đồ
                    points = lesson['content'].split('.')
                    cols = st.columns(2)
                    for i, p in enumerate([pt for pt in points if len(pt) > 5]):
                        with cols[i % 2]:
                            st.info(p.strip())

    # 2. NẾU LÀ QUIZ/TEST
    else:
        idx = st.session_state.current_idx
        if idx < len(data) and idx < 20:
            q = data[idx]
            st.write(f"### Câu {idx + 1}")
            st.info(q.get('question'))
            
            for i, opt in enumerate(q.get('options', [])):
                if st.button(opt, key=f"q_{idx}_{i}"):
                    if i == q.get('answer'):
                        st.success("Đúng rồi! ✨")
                        st.session_state.score += 1
                    else:
                        st.error(f"Sai rồi! Đáp án là: {q['options'][q['answer']]}")
                    st.session_state.current_idx += 1
                    st.rerun()
        else:
            st.balloons()
            st.success(f"Hoàn thành! Điểm của bạn: {st.session_state.score}/{idx}")
            if st.button("LÀM LẠI"):
                st.session_state.page = 'select'
                st.rerun()
