import streamlit as st
import requests
from gtts import gTTS
import re
from io import BytesIO

# API Key Streamlit Secrets se lega
API_KEY = st.secrets["AIzaSyB2WoX0n6vuDO8LeP7vzzv7vE731E9MO9E"]

st.set_page_config(page_title="ShikshaGPT", page_icon="🔥")
st.title("ShikshaGPT Pro Max 🔥")
st.write("8th + 10th CBSE ka AI Teacher | Sawaal poocho, awaaz me suno")

def gemini_pucho(sawal, class_level):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    prompt = f"""Tu ShikshaGPT hai. User {class_level} CBSE ka student hai.
    Pehle 1 line me bata ki ye kaunsa subject aur chapter hai.
    Phir sawaal ko Hinglish me 3-4 line me simple samjha.
    ** ya # mat use karna.
    Sawal: {sawal}"""

    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, json=data, timeout=60)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        elif response.status_code == 429:
            return "Bhai 1 din ka quota khatam. Kal try karna."
        else:
            return f"Error {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def text_ko_audio_banao(text):
    try:
        saaf_text = re.sub(r'[\*#]+','', text)
        tts = gTTS(text=saaf_text, lang='hi', slow=True, tld='co.in')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        st.error(f"Audio Error: {e}")
        return None

# UI Start
class_level = st.selectbox("Class Choose Karo:", ["10th", "8th"])
sawal = st.text_input("Apna Sawaal Yahan Likho:", placeholder="Bal gobin bhagat samjha")
speed = st.radio("Awaaz ki Speed:", ["Slow", "Fast"])

if st.button("Jawab Do 🔥"):
    if sawal:
        with st.spinner("ShikshaGPT soch raha hai..."):
            jawab = gemini_pucho(sawal, class_level)

        st.subheader("Jawab:")
        st.success(jawab)

        with st.spinner("Awaaz bana raha hu..."):
            audio_file = text_ko_audio_banao(jawab)
            if audio_file:
                st.audio(audio_file, format='audio/mp3')
                st.info("👆 Play button daba ke suno")
    else:
        st.warning("Pehle sawaal to likh bhai 😂")

st.markdown("---")
st.caption("Made with ❤️ by You | ShikshaGPT Pro Max")
