import streamlit as st
import ollama

st.title("🌍 AI Text Translator Offline")

# Pakai model Llama 3.1 8B
# Pastikan Anda sudah menginstall Ollama dan model Llama 3.1 8B
model_name = "llama3.1:8b"

# Membuat chat history dan messages di session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a professional multilingual translator. "
                "Your job is to accurately translate any text provided to you. "
                "Preserve the tone, meaning, and style. Only return the translated version, without explanations."
            )
        }
    ]

# Menampilkan chat history
for user_msg, bot_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

# Input chat dari pengguna
query = st.chat_input("Contoh: terjemahkan ke dalam bahasa spanyol, 'Halo apa kabar?'")

if query:
    # Simpan pesan pengguna ke dalam session state
    with st.chat_message("user"):
        st.markdown(query)

    # Tambahkan pesan pengguna ke dalam messages untuk model
    st.session_state.messages.append({"role": "user", "content": query})

    # Menggunakan Ollama untuk mendapatkan respons dari model
    with st.chat_message("assistant"):
        response_stream = ollama.chat(
            model=model_name,
            messages=st.session_state.messages,
            stream=True
        )
        answer = ""
        response_placeholder = st.empty()
        # Proses streaming respons (Proses ini ketikan streamning seperti chatGPT)
        for chunk in response_stream:
            content = chunk.get("message", {}).get("content", "")
            answer += content
            response_placeholder.markdown(answer)
    
    # Setelah selesai, simpan respons ke dalam session state
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.chat_history.append((query, answer))
