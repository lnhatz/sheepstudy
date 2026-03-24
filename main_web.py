import streamlit as st
import json
import random
import os

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Sheep Study", page_icon="✿", layout="wide")

CORAL_PINK = "#ff6b86"

# CSS làm nút bấm đẹp và tràn màn hình
st.markdown(f"""
    <style>
    .stButton>button {{
        width: 100%;
        border-radius: 20px;
        height: 3.5em;
        background-color: {CORAL_PINK};
        color: white;
        font-weight: bold;
        font-size: 18px;
    }}
    .main-title {{
        text-align: center;
        color: {CORAL_PINK};
        font-size: 60px;
        font-weight: bold;
        margin-bottom: 0px;
    }}
    </style>
    """, unsafe_allow_html=True)

# Khởi tạo các biến lưu trữ trạng thái
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0

def load_data(grade, subject, mode):
    # subject ở đây là 'toan' hoặc 'khtn' (viết thường)
    # Thêm lớp thư mục subject vào giữa để đúng cấu trúc của bạn
    fname = f"data/{subject}/{grade}_{mode}.json"
    
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Dòng này để debug nếu vẫn lỗi, nó sẽ in ra đường dẫn mà code đang thử tìm
    st.error(f"Không tìm thấy file tại: {fname}")
    return []

# --- TRANG CHÀO MỪNG ---
if st.session_state.page == 'welcome':
    st.markdown('<p class="main-title">✿ SHEEP STUDY ✿</p>', unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Hệ thống ôn tập thông minh cho học sinh</p>", unsafe_allow_html=True)
    st.write("---")
    if st.button("BẮT ĐẦU HỌC ♡"):
        st.session_state.page = 'select'
        st.rerun()

# --- TRANG CHỌN CHẾ ĐỘ ---
elif st.session_state.page == 'select':
    st.markdown(f"<h2 style='color: {CORAL_PINK};'>THIẾT LẬP ÔN TẬP</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        subject_name = st.selectbox("Chọn môn học", ["Toán", "KHTN"])
        subject_code = "toan" if subject_name == "Toán" else "khtn"
    with col2:
        grade = st.selectbox("Chọn lớp", ["6", "7", "8", "9"])
    
    # THÊM ĐỦ 3 CHẾ ĐỘ Ở ĐÂY
    mode_name = st.radio("Chế độ", ["Luyện tập (Quiz)", "Kiểm tra (Test)", "Lý thuyết (Theory)"], horizontal=True)
    mode_code = "quiz" if "Quiz" in mode_name else "test" if "Test" in mode_name else "theory"
    
    st.write("---")
    if st.button("VÀO HỌC NGAY", use_container_width=True):
        data = load_data(grade, subject_code, mode_code)
        if data:
            st.session_state.data = data
            random.shuffle(st.session_state.data)
            st.session_state.page = 'doing'
            st.session_state.current_idx = 0
            st.session_state.score = 0
            st.rerun()
        else:
            st.error(f"Không tìm thấy dữ liệu cho Lớp {grade} môn {subject_name} chế độ {mode_name}. Bạn đã up file JSON vào thư mục data chưa?")

# --- TRANG LÀM BÀI (HIỂN THỊ CÂU HỎI) ---
elif st.session_state.page == 'doing':
    data = st.session_state.data
    idx = st.session_state.current_idx
    
    if idx < len(data) and idx < 10:
        q = data[idx]
        st.progress((idx + 1) / 10)
        st.info(f"Câu hỏi {idx + 1}: {q['question']}")
        
        for i, opt in enumerate(q['options']):
            if st.button(opt, key=f"opt_{idx}_{i}"):
                if i == q['answer']:
                    st.success("Chính xác! ✨")
                    st.session_state.score += 1
                else:
                    st.error(f"Sai rồi! Đáp án đúng là: {q['options'][q['answer']]}")
                
                # Tự động chuyển câu sau 1 giây hoặc khi bấm nút
                st.session_state.current_idx += 1
                st.rerun()
    else:
        st.balloons()
        st.markdown(f"## HOÀN THÀNH! ĐIỂM: {st.session_state.score}/{idx}")
        if st.button("LÀM LẠI"):
            st.session_state.page = 'welcome'
            st.rerun()

# --- TRANG LÝ THUYẾT (SƠ ĐỒ BÀI HỌC) ---
elif st.session_state.page == 'doing' and st.session_state.mode == 'theory':
    data = st.session_state.data
    st.markdown(f"<h2 style='text-align: center; color: {CORAL_PINK};'>📂 THƯ VIỆN LÝ THUYẾT</h2>", unsafe_allow_html=True)
    
    if st.button("← QUAY LẠI CHỌN MÔN"):
        st.session_state.page = 'select'
        st.rerun()

    for chapter in data:
        with st.expander(f"📖 {chapter.get('title', 'Chương')}", expanded=True):
            for lesson in chapter.get('lessons', []):
                st.markdown(f"#### 🌿 {lesson['name']}")
                
                # Biến nội dung thành các hộp ghi chú (thay cho node sơ đồ)
                points = [p.strip() for p in lesson['content'].split('\n') if p.strip()]
                cols = st.columns(3) # Chia làm 3 cột cho đẹp
                for idx, point in enumerate(points):
                    with cols[idx % 3]:
                        st.info(point)
                st.write("---")
