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
        subject = st.selectbox("Chọn môn học", ["Toán", "KHTN"])
    with col2:
        grade = st.selectbox("Chọn lớp", ["6", "7", "8", "9"])
    
    mode = st.radio("Chế độ", ["Luyện tập (Quiz)", "Lý thuyết (Theory)"])
    
    if st.button("VÀO HỌC NGAY", use_container_width=True):
        # Logic chuyển trang ở đây
        st.success(f"Đang tải dữ liệu {subject} lớp {grade}...")
