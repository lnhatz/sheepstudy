import streamlit as st
import json
import random
import os
import time

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Sheep Study", page_icon="✿", layout="wide")

CORAL_PINK = "#ff6b86"

# --- 2. CSS FIX LỖI MẤT MẢNH TRÊN & HIỆU ỨNG KÍNH MỜ ---
st.markdown(f"""
    <style>
    #MainMenu {{ {{visibility: hidden;}} }}
    header {{ {{visibility: hidden;}} }}
    footer {{ {{visibility: hidden;}} }}
    [data-testid="stHeader"] {{ {{display: none;}} }}

    .stApp {{
        background-image: url("https://png.pngtree.com/background/20250606/original/pngtree-back-to-school-artistic-background-picture-image_16624609.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .block-container {{
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 3rem !important;
        margin-top: 5vh !important;
        margin-bottom: 5vh !important;
        max-width: 950px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. KHỞI TẠO SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 'select'
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'temp_choice' not in st.session_state: st.session_state.temp_choice = None
if 'questions' not in st.session_state: st.session_state.questions = []
if 'mode' not in st.session_state: st.session_state.mode = None
# CHÈN THÊM BIẾN THỜI GIAN
if 'start_time' not in st.session_state: st.session_state.start_time = None

def load_data(grade):
    file_path = f"{grade}_theory.json"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# --- 4. GIAO DIỆN ---
if st.session_state.page == 'select':
    st.markdown("<h1 style='text-align: center; color: #ff6b86;'>✿ SHEEP STUDY ✿</h1>", unsafe_allow_html=True)
    st.write("### Chọn khối lớp của bạn:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("LỚP 7", use_container_width=True):
            st.session_state.grade = 7
            st.session_state.page = 'main'
            st.rerun()
    with col2:
        if st.button("LỚP 8 (Coming Soon)", use_container_width=True, disabled=True): pass
    with col3:
        if st.button("LỚP 9", use_container_width=True):
            st.session_state.grade = 9
            st.session_state.page = 'main'
            st.rerun()

elif st.session_state.page == 'main':
    data = load_data(st.session_state.grade)
    
    st.sidebar.title(f"Lớp {st.session_state.grade}")
    if st.sidebar.button("Quay lại chọn lớp"):
        st.session_state.page = 'select'
        st.rerun()
    
    tab1, tab2 = st.tabs(["📚 LÝ THUYẾT", "📝 TRẮC NGHIỆM"])

    with tab1:
        for chapter in data:
            with st.expander(chapter['title']):
                for lesson in chapter['lessons']:
                    st.markdown(f"**{lesson['name']}**")
                    st.write(lesson['content'])
                    st.markdown("---")

    with tab2:
        if st.session_state.mode is None:
            st.write("### Bạn muốn làm gì?")
            c1, c2 = st.columns(2)
            if c1.button("LUYỆN TẬP (Không giới hạn)", use_container_width=True):
                st.session_state.mode = 'practice'
                st.session_state.current_idx = 0
                st.session_state.score = 0
                all_q = []
                for ch in data:
                    if 'quiz' in ch: all_q.extend(ch['quiz'])
                st.session_state.questions = random.sample(all_q, min(10, len(all_q))) if all_q else []
                st.rerun()
            if c2.button("KIỂM TRA (15 phút - Tự nộp bài)", use_container_width=True):
                st.session_state.mode = 'test'
                st.session_state.current_idx = 0
                st.session_state.score = 0
                st.session_state.start_time = time.time() # GHI LẠI THỜI GIAN BẮT ĐẦU
                all_q = []
                for ch in data:
                    if 'quiz' in ch: all_q.extend(ch['quiz'])
                st.session_state.questions = random.sample(all_q, min(10, len(all_q))) if all_q else []
                st.rerun()
        else:
            questions = st.session_state.questions
            total_q = len(questions)

            # --- LOGIC ĐỒNG HỒ TỰ NỘP BÀI ---
            if st.session_state.mode == 'test' and st.session_state.current_idx < total_q:
                limit = 15 * 60
                elapsed = time.time() - st.session_state.start_time
                remain = max(0, limit - int(elapsed))
                m, s = divmod(remain, 60)
                
                # Hiển thị đồng hồ (Style tối giản để không phá layout của bro)
                st.markdown(f"<p style='text-align: right; color: {'red' if remain < 60 else CORAL_PINK}; font-weight: bold;'>⏳ {m:02d}:{s:02d}</p>", unsafe_allow_html=True)
                
                if remain <= 0:
                    st.error("Hết thời gian! Đang tự động nộp bài...")
                    time.sleep(2)
                    st.session_state.current_idx = total_q
                    st.rerun()

            if st.session_state.current_idx < total_q:
                idx = st.session_state.current_idx
                q = questions[idx]
                
                st.write(f"### Câu {idx + 1}/{total_q}")
                st.info(q.get('question'))
                
                cols = st.columns(2)
                for i, opt in enumerate(q.get('options', [])):
                    with cols[i % 2]:
                        if st.button(opt, key=f"q_{idx}_{i}", 
                                    type="primary" if st.session_state.temp_choice == i else "secondary",
                                    use_container_width=True):
                            st.session_state.temp_choice = i
                            st.rerun()

                st.markdown("---")
                if st.session_state.temp_choice is not None:
                    if st.button("XÁC NHẬN TRẢ LỜI", use_container_width=True):
                        if st.session_state.temp_choice == q.get('answer'):
                            st.success("Đúng rồi!")
                            st.session_state.score += 1
                        else:
                            st.error(f"Sai rồi! Đáp án đúng: {q['options'][q['answer']]}")
                        time.sleep(0.8) 
                        st.session_state.current_idx += 1
                        st.session_state.temp_choice = None
                        st.rerun()
                else:
                    st.warning("Vui lòng chọn 1 đáp án.")
            else:
                st.balloons()
                st.markdown(f"<div style='text-align: center;'><h1>🏆 HOÀN THÀNH!</h1><h2>Điểm số: {st.session_state.score} / {total_q}</h2></div>", unsafe_allow_html=True)
                if st.button("Quay lại"):
                    st.session_state.page = 'select'
                    st.session_state.mode = None # Reset mode khi xong
                    st.rerun()
