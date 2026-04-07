import streamlit as st
import joblib
import io
from gtts import gTTS
from PIL import Image
import os

# ---------- BASE PATH ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- UI TEXT (ALL LANGUAGES) ----------
ui_text = {
    "English": {
        "select_lang": "🌐 Select Language",
        "nav": "📌 Navigation",
        "welcome": "👋 Welcome to AI Cyber Safety Teacher",
        "welcome_msg": "Learn how to stay safe online.",
        "attack_title": "📌 Cyber Attack Types",
        "demo_title": "🔍 Demo / Manual Message Analysis",
        "input": "📩 Enter message / call content",
        "analyze": "🔍 Analyze",
        "clear": "🧹 Clear",
        "empty": "⚠️ Please enter some text",
        "safe": "Be cautious"
    },
    "Hindi": {
        "select_lang": "🌐 भाषा चुनें",
        "nav": "📌 नेविगेशन",
        "welcome": "👋 AI साइबर सुरक्षा शिक्षक में आपका स्वागत है",
        "welcome_msg": "ऑनलाइन सुरक्षित रहना सीखें।",
        "attack_title": "📌 साइबर हमले के प्रकार",
        "demo_title": "🔍 संदेश विश्लेषण",
        "input": "📩 संदेश / कॉल लिखें",
        "analyze": "🔍 विश्लेषण करें",
        "clear": "🧹 साफ करें",
        "empty": "⚠️ कृपया कुछ लिखें",
        "safe": "सतर्क रहें"
    },
    "Kannada": {
        "select_lang": "🌐 ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ",
        "nav": "📌 ನ್ಯಾವಿಗೇಶನ್",
        "welcome": "👋 AI ಸೈಬರ್ ಸುರಕ್ಷತಾ ಶಿಕ್ಷಕರಿಗೆ ಸ್ವಾಗತ",
        "welcome_msg": "ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಸುರಕ್ಷಿತವಾಗಿರಲು ಕಲಿಯಿರಿ.",
        "attack_title": "📌 ಸೈಬರ್ ದಾಳಿ ಪ್ರಕಾರಗಳು",
        "demo_title": "🔍 ಸಂದೇಶ ವಿಶ್ಲೇಷಣೆ",
        "input": "📩 ಸಂದೇಶ / ಕರೆ ಬರೆಯಿರಿ",
        "analyze": "🔍 ವಿಶ್ಲೇಷಿಸಿ",
        "clear": "🧹 ತೆರವುಗೊಳಿಸಿ",
        "empty": "⚠️ ದಯವಿಟ್ಟು ಕೆಲವು ಪಠ್ಯ ನಮೂದಿಸಿ",
        "safe": "ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"
    }
}

# ---------- IMAGE FUNCTION ----------
def display_centered_image(image_name, width=250):
    path = os.path.join(BASE_DIR, image_name)
    if os.path.exists(path):
        img = Image.open(path)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(img, width=width)

# ---------- AUDIO ----------
def speak(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp)

# ---------- LOAD MODEL ----------
try:
    model, vectorizer = joblib.load(os.path.join(BASE_DIR, "cyber_model.pkl"))
    model_loaded = True
except:
    model_loaded = False

def predict(text):
    if not model_loaded:
        return "unknown"
    return model.predict(vectorizer.transform([text]))[0]

# ---------- FEEDBACK ----------
feedback = {
    "phishing":{"English":"⚠️ Phishing! Avoid links","Hindi":"⚠️ फ़िशिंग! लिंक से बचें","Kannada":"⚠️ ಫಿಶಿಂಗ್! ಲಿಂಕ್ ತಪ್ಪಿಸಿ"},
    "otp_fraud":{"English":"⚠️ OTP Fraud! Never share","Hindi":"⚠️ OTP धोखाधड़ी! साझा न करें","Kannada":"⚠️ OTP ಮೋಸ! ಹಂಚಬೇಡಿ"},
}

# ---------- LANGUAGE ----------
lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
t = ui_text[lang]
lang_code = {"English":"en","Hindi":"hi","Kannada":"kn"}[lang]

# ---------- NAV ----------
st.sidebar.header(t["nav"])
page = st.sidebar.radio("", ["Welcome","Cyber Attack Details","Demo"])

# ---------- WELCOME ----------
if page=="Welcome":
    display_centered_image("welcome_image.jpeg", 350)
    st.header(t["welcome"])
    st.write(t["welcome_msg"])
    speak(t["welcome_msg"], lang_code)

# ---------- ATTACK DETAILS ----------
elif page=="Cyber Attack Details":
    display_centered_image("ai_teacher_logo.jpeg", 250)
    st.header(t["attack_title"])

    attacks = {
        "phishing":{"English":"Fake links","Hindi":"नकली लिंक","Kannada":"ನಕಲಿ ಲಿಂಕ್"},
        "otp_fraud":{"English":"OTP scams","Hindi":"OTP धोखाधड़ी","Kannada":"OTP ಮೋಸ"}
    }

    for k,v in attacks.items():
        st.write(f"• {k}: {v[lang]}")
        speak(v[lang], lang_code)

# ---------- DEMO ----------
elif page=="Demo":
    display_centered_image("ai_teacher_logo.jpeg", 250)
    st.header(t["demo_title"])

    user_input = st.text_area(t["input"])

    col1,col2 = st.columns(2)
    with col1:
        check = st.button(t["analyze"])
    with col2:
        clear = st.button(t["clear"])

    if clear:
        st.experimental_rerun()

    if check:
        if user_input.strip()=="":
            st.warning(t["empty"])
            speak(t["empty"], lang_code)
        else:
            cat = predict(user_input)
            msg = feedback.get(cat, {
                "English":t["safe"],
                "Hindi":t["safe"],
                "Kannada":t["safe"]
            })[lang]

            st.error(msg)
            speak(msg, lang_code)
