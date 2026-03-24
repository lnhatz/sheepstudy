import streamlit as st
import json
import random
import os

# --- CẤU HÌNH ---
st.set_page_config(page_title="Sheep Study", page_icon="✿", layout="wide")

CORAL_PINK = "#ff6b86"
SOFT_BLUE = "#e1f5fe"

# CSS ĐẶC BIỆT ĐỂ TẠO CẢM GIÁC SƠ ĐỒ
st.markdown(f"""
    <style>
    /* Giấu sạch dấu vết của Streamlit */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stHeader"] {{display: none;}}
    
    .stButton>button {{
        width: 100%; border-radius: 15px; background-color: {CORAL_PINK}; color: white; font-weight: bold;
    }}
    .mindmap-node {{
        background-color: white; border: 2px solid {CORAL_PINK}; border-radius: 10px; padding: 15px; margin-bottom: 10px;
    }}
    .main-title {{
        text-align: center; color: {CORAL_PINK}; font-size: 50px; font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'welcome'

def load_data(grade, subject, mode):
    fname = f"data/{subject}/{grade}_{mode}.json"
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# --- TRANG CHÀO MỪNG ---
if st.session_state.page == 'welcome':
    st.markdown(f"<h1 style='text-align: center; color: {CORAL_PINK};'>✿ SHEEP STUDY ✿</h1>", unsafe_allow_html=True)
    if st.button("BẮT ĐẦU HÀNH TRÌNH HỌC TẬP ♡"):
        st.session_state.page = 'select'
        st.rerun()

# --- TRANG CHỌN CHẾ ĐỘ ---
elif st.session_state.page == 'select':
    st.markdown(f"<h2 style='color: {CORAL_PINK};'>LỰA CHỌN BÀI HỌC</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        sb_name = st.selectbox("Môn học", ["Toán", "KHTN"])
        subject = "toan" if sb_name == "Toán" else "khtn"
    with c2:
        grade = st.selectbox("Lớp", ["6", "7", "8", "9"])
    
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
            st.error(f"⚠️ Thiếu file: data/{subject}/{grade}_{mode}.json")

# --- TRANG HIỂN THỊ NỘI DUNG ---
elif st.session_state.page == 'doing':
    if st.button("← QUAY LẠI"):
        st.session_state.page = 'select'
        st.rerun()

    data = st.session_state.data
    
    # --- PHẦN LÝ THUYẾT (MINDMAP WEB STYLE) ---
    if st.session_state.mode == 'theory':
        for chapter in data:
            st.markdown(f"<div class='chapter-title'>📂 {chapter.get('title')}</div>", unsafe_allow_html=True)
            
            for lesson in chapter.get('lessons', []):
                with st.expander(f"🌿 {lesson['name']}", expanded=False):
                    # Tách các ý chính
                    points = [p.strip() for p in lesson['content'].split('.') if len(p.strip()) > 5]
                    
                    # Hiển thị trung tâm
                    st.markdown(f"<div class='mindmap-node' style='background-color: {SOFT_BLUE}; font-weight: bold;'>{lesson['name']}</div>", unsafe_allow_html=True)
                    
                    # Tỏa ra các nhánh (chia cột)
                    cols = st.columns(2)
                    for i, point in enumerate(points):
                        with cols[i % 2]:
                            st.markdown(f"<div class='mindmap-node'>📍 {point}</div>", unsafe_allow_html=True)

    # --- PHẦN TRẮC NGHIỆM ---
    else:
        idx = st.session_state.current_idx
        if idx < len(data) and idx < 20:
            q = data[idx]
            st.markdown(f"### Câu {idx + 1}")
            st.info(q.get('question'))
            
            for i, opt in enumerate(q.get('options', [])):
                if st.button(opt, key=f"q_{idx}_{i}"):
                    if i == q.get('answer'):
                        st.success("Quá giỏi! ✨")
                        st.session_state.score += 1
                    else:
                        st.error(f"Tiếc quá! Đáp án đúng là: {q['options'][q['answer']]}")
                    st.session_state.current_idx += 1
                    st.rerun()
        else:
            st.balloons()
            st.success(f"🎊 HOÀN THÀNH! ĐIỂM CỦA BẠN: {st.session_state.score}/{idx}")
            if st.button("LÀM LẠI TỪ ĐẦU"):
                st.session_state.page = 'select'
                st.rerun()
