import streamlit as st
import json
import random
import os

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Sheep Study", page_icon="✿", layout="wide")

CORAL_PINK = "#ff6b86"
SOFT_BLUE = "#e1f5fe"

# --- 2. CSS TRANG TRÍ ---
st.markdown(f"""
    <style>
    /* Giấu sạch dấu vết hệ thống */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stHeader"] {{display: none;}}

    /* Căn giữa cụm chứa nút bấm */
    div.stButton {{
        display: flex;
        justify-content: center;
    }}

    /* Thiết kế nút bấm chuyên nghiệp */
    .stButton>button {{
        width: 100% !important;
        max-width: 400px;
        min-height: 70px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        border-radius: 15px !important;
        background-color: {CORAL_PINK} !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: none !important;
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0px 4px 15px rgba(255, 107, 134, 0.4);
    }}

    .theory-node {{
        background-color: white;
        border: 2px solid {CORAL_PINK};
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: center;
    }}

    .main-title {{
        text-align: center; color: {CORAL_PINK}; font-size: 45px; font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. KHỞI TẠO BIẾN TẠM (SESSION STATE) ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'data' not in st.session_state: st.session_state.data = []
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'mode' not in st.session_state: st.session_state.mode = ''

# --- 4. HÀM LOAD DỮ LIỆU ---
def load_data(grade, subject, mode):
    path = f"data/{grade}_{mode}.json"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# --- 5. ĐIỀU HƯỚNG TRANG ---
# A. TRANG CHÀO MỪNG
if st.session_state.page == 'welcome':
    st.markdown('<p class="main-title">✿ SHEEP STUDY ✿</p>', unsafe_allow_html=True)
    st.write("<p style='text-align: center; font-size: 20px;'>Học tập thông minh cùng Cừu nhỏ!</p>", unsafe_allow_html=True)
    
    if st.button("BẮT ĐẦU HỌC"):
        st.session_state.page = 'select'
        st.rerun()

# B. TRANG CHỌN MÔN & CHƯƠNG
elif st.session_state.page == 'select':
    st.markdown(f"<h2 style='color: {CORAL_PINK}; text-align: center;'>LỰA CHỌN MÔN HỌC</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        sb_name = st.selectbox("Môn học", ["Toán", "KHTN"])
        subject = "toan" if sb_name == "Toán" else "khtn"
    with c2:
        grade = st.selectbox("Lớp", ["6", "7", "8", "9"])
    
    mode_name = st.radio("Chế độ", ["Lý thuyết", "Trắc nghiệm", "Kiểm tra"], horizontal=True)
    mode = "theory" if "Lý thuyết" in mode_name else "quiz" if "Trắc nghiệm" in mode_name else "test"
    
    # Logic quét chương
    res = load_data(grade, subject, mode)
    selected_chapter = "Tất cả"
    
    if res and mode != 'theory':
        chapters = list(set([q.get('chapter', 'Chưa phân loại') for q in res]))
        chapters.sort()
        chapters.insert(0, "Tất cả")
        selected_chapter = st.selectbox("Chọn Chương muốn ôn tập:", chapters)
    
    if st.button("VÀO HỌC"):
        if res:
            if mode != 'theory':
                # Lọc theo chương
                if selected_chapter != "Tất cả":
                    st.session_state.data = [q for q in res if q.get('chapter') == selected_chapter]
                else:
                    st.session_state.data = res
                random.shuffle(st.session_state.data)
            else:
                st.session_state.data = res
                
            st.session_state.mode = mode
            st.session_state.page = 'doing'
            st.session_state.current_idx = 0
            st.session_state.score = 0
            st.rerun()
        else:
            st.error("⚠️ Chưa có dữ liệu cho phần này!")

# C. TRANG NỘI DUNG (HỌC/THI)
elif st.session_state.page == 'doing':
    data = st.session_state.data
    mode = st.session_state.mode
    
    if st.button("⬅ Quay lại"):
        st.session_state.page = 'select'
        st.rerun()

    if mode == 'theory':
        for chapter in data:
            st.markdown(f"### 📂 {chapter.get('title')}")
            for lesson in chapter.get('lessons', []):
                with st.expander(f"🌿 {lesson['name']}"):
                    points = [p.strip() for p in lesson['content'].split('.') if len(p.strip()) > 5]
                    cols = st.columns(2)
                    for i, pt in enumerate(points):
                        with cols[i % 2]:
                            st.markdown(f"<div class='theory-node'>📍 {pt}</div>", unsafe_allow_html=True)
    else:
        idx = st.session_state.current_idx
        # Giới hạn 20 câu hoặc ít hơn nếu bộ đề ngắn
        total_q = min(len(data), 20)
        
        if idx < total_q:
            # Hiển thị số câu và thanh tiến trình
            st.write(f"📝 **Tiến độ: {idx + 1} / {total_q}**")
            st.progress((idx + 1) / total_q)
            
            q = data[idx]
            st.info(f"Câu {idx + 1}: {q.get('question')}")
            
            cols = st.columns(2)
            for i, opt in enumerate(q.get('options', [])):
                with cols[i % 2]:
                    if st.button(opt, key=f"q_{idx}_{i}"):
                        if i == q.get('answer'):
                            st.success("Đúng rồi!")
                            st.session_state.score += 1
                        else:
                            st.error(f"Sai rồi! Đáp án: {q['options'][q['answer']]}")
                        st.session_state.current_idx += 1
                        st.rerun()
        else:
            st.balloons()
            st.success(f"🏆 Hoàn thành! Điểm của bạn: {st.session_state.score}/{total_q}")
            if st.button("Làm lại từ đầu"):
                st.session_state.page = 'select'
                st.rerun()
