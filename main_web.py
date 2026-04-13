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
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    .main-title {{
        text-align: center;
        color: {CORAL_PINK};
        font-size: clamp(35px, 7vw, 70px) !important;
        font-weight: 900;
        line-height: 1.2;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        word-wrap: break-word;
    }}

    .theory-node {{
        background-color: white;
        border: 2px solid {CORAL_PINK};
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: center;
    }}

    div.stButton {{
        display: flex;
        justify-content: center;
    }}

    .stButton > button {{
        width: 100% !important;
        max-width: 450px;
        min-height: 65px !important;
        border-radius: 20px !important;
        background-color: {CORAL_PINK} !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: none !important;
        transition: 0.3s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0px 5px 15px rgba(255, 107, 134, 0.4);
    }}

    .stButton > button[kind="secondary"] {{
        background-color: white !important;
        color: {CORAL_PINK} !important;
        border: 2px solid {CORAL_PINK} !important;
    }}

    .timer-box {{
        padding: 10px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        background: white;
        border: 2px solid {CORAL_PINK};
        margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC HỆ THỐNG ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'temp_choice' not in st.session_state: st.session_state.temp_choice = None
if 'end_time' not in st.session_state: st.session_state.end_time = None

def load_data(grade, subject, mode):
    fname = f"data/{{subject}}/{{grade}}_{{mode}}.json".format(subject=subject, grade=grade, mode=mode)
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# --- 4. CÁC TRANG ---
if st.session_state.page == 'welcome':
    st.markdown('<p class="main-title">✿ SHEEP STUDY ✿</p>', unsafe_allow_html=True)
    st.write("<p style='text-align: center; font-size: 20px; color: #444;'>Học không khó, đã có sheep lo!</p>", unsafe_allow_html=True)
    
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
    
    mode_name = st.radio("Chế độ", ["Lý thuyết", "Trắc nghiệm", "Kiểm tra"], horizontal=True)
    mode = "theory" if "Lý thuyết" in mode_name else "quiz" if "Trắc nghiệm" in mode_name else "test"
    
    res = load_data(grade, subject, mode)
    selected_chapter = "Tất cả"
    if res and mode != 'theory':
        chapters = sorted(list(set([q.get('chapter', 'Khác') for q in res])))
        chapters.insert(0, "Tất cả")
        selected_chapter = st.selectbox("Chọn Chương muốn ôn tập:", chapters)

    if st.button("VÀO HỌC"):
        if res:
            if mode != 'theory':
                temp_data = [q for q in res if q.get('chapter') == selected_chapter] if selected_chapter != "Tất cả" else res
                # TRỘN THỨ TỰ CÂU HỎI
                random.shuffle(temp_data)
                
                # LOGIC TRỘN ĐÁP ÁN (BẢO TOÀN ĐÁP ÁN ĐÚNG)
                for question in temp_data:
                    opts = question['options']
                    correct_text = opts[question['answer']]
                    random.shuffle(opts)
                    question['answer'] = opts.index(correct_text)
                
                st.session_state.data = temp_data
            else:
                st.session_state.data = res
            
            st.session_state.mode, st.session_state.page = mode, 'doing'
            st.session_state.current_idx, st.session_state.score = 0, 0
            st.session_state.temp_choice = None
            st.session_state.end_time = time.time() + 600 
            st.rerun()
        else:
            st.error(f"⚠️ Không tìm thấy file dữ liệu.")

elif st.session_state.page == 'doing':
    data = st.session_state.data
    mode = st.session_state.mode
    
    if mode == 'test':
        remaining = max(0, int(st.session_state.end_time - time.time()))
        mins, secs = divmod(remaining, 60)
        st.markdown(f'<div class="timer-box">⏱️ Thời gian còn lại: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        if remaining <= 0:
            st.session_state.current_idx = 999 
            st.rerun()

    if mode == 'theory':
        if st.button("⬅ QUAY LẠI"): st.session_state.page = 'select'; st.rerun()
        search_query = st.text_input("🔍 Tìm kiếm từ khóa").lower()
        st.markdown("---")
        found_any = False
        for chapter in data:
            filtered = [ls for ls in chapter.get('lessons', []) if search_query in ls['name'].lower() or search_query in ls['content'].lower()]
            if filtered:
                found_any = True
                st.markdown(f"### 📂 {chapter.get('title')}")
                for lesson in filtered:
                    with st.expander(f"🌿 {lesson['name']}"):
                        points = [p.strip() for p in lesson['content'].split('.') if len(p.strip()) > 5]
                        cols = st.columns(2)
                        for i, pt in enumerate(points):
                            with cols[i % 2]: st.markdown(f"<div class='theory-node'>📍 {pt}</div>", unsafe_allow_html=True)
        if not found_any: st.warning("Không tìm thấy kết quả.")

    else:
        idx = st.session_state.current_idx
        total_q = min(len(data), 20)
        
        if idx < total_q:
            if st.button("⬅ QUAY LẠI"): st.session_state.page = 'select'; st.rerun()
            st.write(f"📝 **Tiến độ: {idx + 1} / {total_q}**")
            st.progress((idx + 1) / total_q)
            q = data[idx]
            st.info(f"Câu {idx + 1}: {q.get('question')}")
            
            cols = st.columns(2)
            for i, opt in enumerate(q.get('options', [])):
                with cols[i % 2]:
                    if st.button(opt, key=f"q_{idx}_{i}", type="primary" if st.session_state.temp_choice == i else "secondary", use_container_width=True):
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
                st.rerun()
    
    if mode == 'test' and st.session_state.current_idx < total_q:
        time.sleep(1)
        st.rerun()
