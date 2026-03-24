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
    .stButton>button {{
        width: 100%; border-radius: 15px; background-color: {CORAL_PINK}; color: white; font-weight: bold;
    }}
    .mindmap-node {{
        background-color: white;
        border: 2px solid {CORAL_PINK};
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        text-align: center;
    }}
    .chapter-title {{
        color: {CORAL_PINK};
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        border-bottom: 3px solid {CORAL_PINK};
        padding-bottom: 10px;
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
    
    # --- TRANG HIỂN THỊ LÝ THUYẾT DẠNG SƠ ĐỒ ---
elif st.session_state.page == 'doing' and st.session_state.mode == 'theory':
    st.markdown(f"<h2 style='text-align: center; color: {CORAL_PINK};'>🌿 SƠ ĐỒ TƯ DUY KIẾN THỨC</h2>", unsafe_allow_html=True)
    
    if st.button("← QUAY LẠI CHỌN MÔN"):
        st.session_state.page = 'select'
        st.rerun()

    for idx_ch, chapter in enumerate(st.session_state.data):
        # 1. Tạo ID và Text an toàn cho Chương
        ch_title = chapter.get('title', 'Chương').replace('"', "'")
        root_id = f"root_{idx_ch}"
        
        mermaid_code = "graph LR\n"
        mermaid_code += f'  {root_id}(("{ch_title}"))\n'
        mermaid_code += f"  style {root_id} fill:{CORAL_PINK},color:#fff,stroke-width:4px\n"

        for i, lesson in enumerate(chapter.get('lessons', [])):
            l_id = f"ch{idx_ch}_l{i}"
            l_name = lesson['name'].replace('"', "'")
            mermaid_code += f'  {root_id} --> {l_id}["{l_name}"]\n'
            
            # 2. Xử lý nội dung bài học để không làm hỏng script
            content = lesson.get('content', '')
            # Tách ý theo dấu chấm hoặc gạch đầu dòng
            raw_points = content.replace('\n', '.').split('.')
            points = [p.strip() for p in raw_points if len(p.strip()) > 5]
            
            for j, pt in enumerate(points[:3]): 
                p_id = f"ch{idx_ch}_l{i}_p{j}"
                # Xóa sạch các ký tự có thể gây lỗi cú pháp Mermaid
                clean_pt = pt.replace('"', "'").replace('(', '').replace(')', '')
                short_text = (clean_pt[:40] + '...') if len(clean_pt) > 40 else clean_pt
                mermaid_code += f'  {l_id} -.-> {p_id}("{short_text}")\n'
        
        st.markdown(f"### 📘 {ch_title}")
        
        # 3. Dùng iframe với cấu trúc chuẩn hơn để tránh trắng màn hình
        html_code = f"""
        <div id="mermaid-{idx_ch}" class="mermaid" style="display: flex; justify-content: center;">
            {mermaid_code}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'base', themeVariables: {{ 'primaryColor': '#ff6b86', 'edgeLabelBackground':'#ffffff' }} }});
        </script>
        """
        st.components.v1.html(html_code, height=500, scrolling=True)

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
