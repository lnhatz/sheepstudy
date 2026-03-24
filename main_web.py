import streamlit as st
import json
import random
import os

# 1. Cấu hình giao diện Web tràn màn hình
st.set_page_config(page_title="SHEEP STUDY", layout="wide")

# 2. Định nghĩa màu sắc 
CORAL_PINK = "#ff6b86"

# 3. Hàm đọc file JSON từ thư mục data
def load_quiz_data(grade, subject, mode):
    # khớp với thư mục  để trên GitHub
    path = f"data/{grade}_{mode}.json" 
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 4. Giao diện chính
st.markdown(f"<h1 style='text-align: center; color: {CORAL_PINK};'>✿ SHEEP STUDY ✿</h1>", unsafe_allow_html=True)

# Khởi tạo trạng thái ứng dụng
if 'page' not in st.session_state: st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.write("### Chào mừng bạn đến với hệ thống ôn tập thông minh!")
    if st.button("BẮT ĐẦU HỌC ♡", use_container_width=True):
        st.session_state.page = 'select'
        st.rerun()

elif st.session_state.page == 'select':
    col1, col2 = st.columns(2)
    with col1:
        subject_name = st.selectbox("Chọn môn học", ["Toán", "KHTN"])
        subject_code = "toan" if subject_name == "Toán" else "khtn"
    with col2:
        grade = st.selectbox("Chọn lớp", ["6", "7", "8", "9"])
    
    # 1. ĐÃ THÊM ĐỦ 3 CHẾ ĐỘ Ở ĐÂY
    mode_name = st.radio("Chế độ", ["Luyện tập (Quiz)", "Kiểm tra (Test)", "Lý thuyết (Theory)"])
    mode_code = "quiz" if "Quiz" in mode_name else "test" if "Test" in mode_name else "theory"
    
    if st.button("VÀO HỌC NGAY", use_container_width=True):
        # Lưu thông tin vào session để dùng ở trang sau
        st.session_state.subject = subject_code
        st.session_state.grade = grade
        st.session_state.mode = mode_code
        
        # 2. LỆNH CHUYỂN TRANG THỰC SỰ
        st.session_state.page = 'doing_task' 
        st.rerun()
