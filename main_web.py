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
    /* Giấu sạch dấu vết hệ thống */
    #MainMenu {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    [data-testid="stHeader"] {{ display: none; }}

    /* Hình nền */
    .stApp {{
        background-image: url("https://png.pngtree.com/background/20250606/original/pngtree-back-to-school-artistic-background-picture-image_16624609.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* KHUNG NỘI DUNG: ĐÃ FIX LỖI MẤT MẢNH TRÊN */
    .block-container {{
        background: rgba(255, 255, 255, 0.85); /* Nền trắng mờ */
        backdrop-filter: blur(10px); /* HIỆU ỨNG KÍNH MỜ NỔI CHỮ */
        border-radius: 25px;
        padding: 3rem !important;
        margin-top: 5vh !important; /* ĐẨY XUỐNG ĐỂ KHÔNG MẤT MẢNH */
        margin-bottom: 5vh !important;
        max-width: 950px !important;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    /* Tiêu đề */
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
if 'start_time' not in st.session_state: st.session_state.start_time = None

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
                st.session_state.data = [q for q in res if q.get('chapter') == selected_chapter] if selected_chapter != "Tất cả" else res
                random.shuffle(st.session_state.data)
            else:
                st.session_state.data = res
            
            st.session_state.mode, st.session_state.page = mode, 'doing'
            st.session_state.current_idx, st.session_state.score = 0, 0
            st.session_state.temp_choice = None
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.error(f"⚠️ Không tìm thấy file dữ liệu.")

elif st.session_state.page == 'doing':
    data = st.session_state.data
    mode = st.session_state.mode
    
    if mode == 'test':
        rem = max(0, 600 - int(time.time() - st.session_state.start_time))
        mins, secs = divmod(rem, 60)
        st.markdown(f'<div class="timer-box">⏱️ Thời gian: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        if rem <= 0: st.session_state.current_idx = 999; st.rerun()

    if mode == 'theory':
        if st.button("⬅ QUAY LẠI"): st.session_state.page = 'select'; st.rerun()
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
                    if st.button(opt, key=f"q_{idx}_{i}", type="primary" if st.session_state.temp_choice == i else "secondary"):
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
            # --- MÀN HÌNH KẾT QUẢ ---
            st.balloons()
            st.markdown(f"<div style='text-align: center;'><h1>🏆 HOÀN THÀNH!</h1><h2>Điểm số: {st.session_state.score} / {total_q}</h2></div>", unsafe_allow_html=True)
            if st.button("Quay lại"):
                st.session_state.page = 'select'
                st.rerun()

# --- 5. GIA SƯ AI THÔNG MINH ---
st.markdown("---")
if "GEMINI_API" in st.secrets:
    import google.generativeai as genai
    genai.configure(api_key=st.secrets["GEMINI_API"])
    model = genai.GenerativeModel('gemini-pro')

    st.subheader("Gia sư Sheep AI")
    user_ask = st.chat_input("Bạn chưa hiểu chỗ nào về bài học này? Hỏi tui đi...")
    
    if user_ask:
        with st.chat_message("assistant"):
            # Lấy 2000 ký tự đầu của dữ liệu làm ngữ cảnh để AI trả lời đúng trọng tâm
            context = str(st.session_state.get('data', ''))[:2000] 
            prompt = f"Dựa trên kiến thức học tập: {context}. Hãy giải thích ngắn gọn cho học sinh: {user_ask}"
            
            response = model.generate_content(prompt)
            st.write(response.text)
else:
    st.info("💡 Mẹo: Nhớ dán API Key vào Streamlit Secrets để kích hoạt gia sư AI nhé!")
