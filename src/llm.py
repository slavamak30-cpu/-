import asyncio
import streamlit as st
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

def generate_answer(question, context_chunks):
    # Объединяем найденные куски в один текст
    context = "\n\n---\n\n".join(context_chunks)
    
    # Улучшенный промпт
    prompt = f"""Ты — эксперт по анализу документов. Твоя задача — найти ответ на вопрос в предоставленном тексте.
Даже если текст выглядит как обрывки, постарайся найти ключевые слова из вопроса и составить ответ.
Если ты видишь, что вопрос касается структуры документа (заголовок, начало), а в тексте этого нет, скажи: "В найденных фрагментах нет заголовка, но вот что есть: [краткий пересказ текста]".

ТЕКСТ ДОКУМЕНТА:
{context}

ВОПРОС: {question}

ОТВЕТ:"""

    try:
        creds = st.secrets["GIGACHAT_CREDENTIALS"]
    except:
        # ВСТАВЬ СЮДА СВОЙ КЛЮЧ ОТ GIGACHAT
        creds = "MDFhMWQ0ZGMtYTFlMC03MGExLWEwNzItZDM1N2NkZmE1NzRjOmM4MGE3MzAzLWY3YjYtNDMxMy1iOWQ5LWExYWJkYmE1ODdiMw=="

    # Исправление ошибки Event Loop для Streamlit
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    try:
        with GigaChat(credentials=creds, scope="GIGACHAT_API_PERS", verify_ssl_certs=False) as client:
            chat = Chat(
                model="GigaChat-2", 
                messages=[Messages(role=MessagesRole.USER, content=prompt)]
            )
            response = client.chat(chat)
            return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка LLM: {e}"