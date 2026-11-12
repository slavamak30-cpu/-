import streamlit as st
import os
import uuid
from src.loader import load_document
from src.chunker import split_text
from src.embedder import add_to_db, search
from src.llm import generate_answer

# 1. Настройка страницы (заголовок, иконка, широкий формат)
st.set_page_config(page_title="RAG Умный помощник", page_icon="🤖", layout="wide")

# 2. Добавляем немного CSS для красоты (кнопки, шрифты)
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
    .big-title {
        text-align: center;
        color: #2E4053;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="big-title">📚 Умный помощник по документам (RAG)</h1>', unsafe_allow_html=True)
st.write("---")

# 3. Делим экран на две колонки
col1, col2 = st.columns([1, 2], gap="large")

# --- ЛЕВАЯ КОЛОНКА (Загрузка) ---
with col1:
    st.subheader("⚙️ 1. Настройки документа")
    uploaded_file = st.file_uploader("Загрузите PDF для анализа", type=["pdf"])
    
    if uploaded_file is not None:
        os.makedirs("data", exist_ok=True)
        
        # Генерация уникального ID
        if "current_doc_id" not in st.session_state:
            st.session_state.current_doc_id = str(uuid.uuid4())[:8]
        
        doc_id = st.session_state.current_doc_id
        unique_filename = f"{doc_id}_{uploaded_file.name}"
        file_path = os.path.join("data", unique_filename)
        
        # Сохранение файла
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.info(f"📄 Файл: **{uploaded_file.name}**\n\n🆔 ID: `{doc_id}`")
        
        # Кнопка обработки
        if st.button("Обработать документ ⚙️", use_container_width=True):
            with st.spinner("Читаем и индексируем..."):
                try:
                    text = load_document(file_path)
                    chunks = split_text(text)
                    add_to_db(chunks, uploaded_file.name, doc_id)
                    st.success(f"✅ Готово! {len(chunks)} фрагментов в базе.")
                except Exception as e:
                    st.error(f"❌ Ошибка: {e}")

    st.write("---")
    st.markdown("### 💡 Инструкция")
    st.markdown("1. Загрузите PDF.\n2. Нажмите 'Обработать'.\n3. Справа задайте вопрос.")

# --- ПРАВАЯ КОЛОНКА (Чат) ---
with col2:
    st.subheader("💬 2. Задайте вопрос")
    question = st.text_input("Введите ваш вопрос по тексту:", placeholder="Например: О чем говорится в главе 2?")
    
    if st.button("Получить ответ 🚀", use_container_width=True):
        if not question:
            st.warning("⚠️ Пожалуйста, введите вопрос.")
        else:
            with st.spinner("Ищем в базе и генерируем ответ..."):
                try:
                    # 1. Поиск
                    docs, metas = search(question, k=3)
                    
                    # 2. Генерация (вызов OpenRouter)
                    answer = generate_answer(question, docs)
                    
                    # 3. Красивый вывод ответа
                    st.markdown("### 🤖 Ответ нейросети:")
                    st.success(answer)
                    
                    # 4. Красивый вывод источников
                    st.markdown("### 📌 Источники:")
                    if metas:
                        for meta in metas:
                            if 'source' in meta and 'doc_id' in meta:
                                st.info(f"📄 Файл: **{meta['source']}** | ID: `{meta['doc_id']}`")
                    else:
                        st.warning("Источники не найдены (возможно, документ не обработан).")
                        
                except Exception as e:
                    st.error(f"❌ Ошибка при ответе: {e}")
                    