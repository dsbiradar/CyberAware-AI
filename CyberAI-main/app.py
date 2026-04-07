import streamlit as st
import joblib
import io
from gtts import gTTS
from PIL import Image
import os
from utils import scenarios

# ---------- Function to display centered images ----------
def display_centered_image(image_path, width=250):
    try:
        if os.path.exists(image_path):
            img = Image.open(image_path)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.image(img, width=width)
        else:
            st.warning(f"Image not found: {image_path}")
    except Exception as e:
        st.warning(f"Error loading image: {e}")

# ---------- Audio function ----------
def speak_streamlit(text, lang_code="en"):
    try:
        tts = gTTS(text=text, lang=lang_code)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        st.audio(mp3_fp, format="audio/mp3")
    except Exception as e:
        st.warning(f"Audio error: {e}")

# ---------- Load model ----------
model_path = "cyber_model.pkl"
model_loaded = False

try:
    model, vectorizer = joblib.load(model_path)   # ✅ FIXED
    model_loaded = True
except Exception as e:
    st.error(f"⚠️ Model not found or error loading: {e}")

# ---------- Prediction ----------
def predict_category(text):
    if not model_loaded:
        speak_streamlit("Model not loaded. Cannot predict.", lang_code="en")
        return "unknown"
    
    text_vec = vectorizer.transform([text])   # ✅ FIXED
    return model.predict(text_vec)[0]

# ---------- Feedback dictionary ----------
feedback_dict = {
    "phishing":{"English":"⚠️ Phishing! Avoid links","Hindi":"⚠️ फ़िशिंग! लिंक से बचें","Kannada":"⚠️ ಫಿಶಿಂಗ್! ಲಿಂಕ್ ತಪ್ಪಿಸಿ"},
    "malware":{"English":"⚠️ Malware detected! Do not install","Hindi":"⚠️ मैलवेयर! इंस्टॉल न करें","Kannada":"⚠️ ಮಾಲ್ವೇರ್ ಕಂಡುಬಂದಿದೆ! ಸ್ಥಾಪಿಸಬೇಡಿ"},
    "ransomware":{"English":"⚠️ Ransomware! Do not pay","Hindi":"⚠️ रैनसमवेयर! भुगतान न करें","Kannada":"⚠️ ರ್ಯಾನ್ಸಮ್‌ವೇರ್! ಪಾವತಿ ಮಾಡಬೇಡಿ"},
    "social_engineering":{"English":"⚠️ Social Engineering! Be alert","Hindi":"⚠️ सोशल इंजिनियरिंग! सतर्क रहें","Kannada":"⚠️ ಸಾಮಾಜಿಕ ಎಂಜಿನಿಯರಿಂಗ್! ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"},
    "password_attack":{"English":"⚠️ Password attack! Keep strong","Hindi":"⚠️ पासवर्ड हमला! मजबूत रखें","Kannada":"⚠️ ಪಾಸ್‌ವರ್ಡ್ ದಾಳಿ! ಬಲವಾಗಿ ಇಡಿ"},
    "otp_fraud":{"English":"⚠️ OTP Fraud! Never share","Hindi":"⚠️ OTP धोखाधड़ी! साझा न करें","Kannada":"⚠️ OTP ಮೋಸ! ಹಂಚಬೇಡಿ"},
    "lottery_scam":{"English":"⚠️ Lottery Scam! Ignore","Hindi":"⚠️ लॉटरी धोखाधड़ी! अनदेखा करें","Kannada":"⚠️ ಲಾಟರಿ ಮೋಸ! ನಿರ್ಲಕ್ಷ್ಯ ಮಾಡಿ"},
    "fake_app":{"English":"⚠️ Fake App! Do not install","Hindi":"⚠️ नकली ऐप! इंस्टॉल न करें","Kannada":"⚠️ ನಕಲಿ ಅಪ್ಲಿಕೇಶನ್! ಸ್ಥಾಪಿಸಬೇಡಿ"},
    "financial_fraud":{"English":"⚠️ Financial Fraud! Be alert","Hindi":"⚠️ वित्तीय धोखाधड़ी! सतर्क रहें","Kannada":"⚠️ ಹಣಕಾಸು ಮೋಸ! ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"},
    "spyware_adware":{"English":"⚠️ Spyware/Adware! Be careful","Hindi":"⚠️ स्पाईवेयर/एडवेयर! सावधान रहें","Kannada":"⚠️ ಸ್ಪೈವೇರ್/ಆಡ್ವೇರ್! ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"}
}

# ---------- Language selection ----------
lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
lang_map_code = {"English":"en","Hindi":"hi","Kannada":"kn"}
lang_code = lang_map_code[lang]

# ---------- Navigation ----------
st.sidebar.header("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Welcome","Cyber Attack Details","Demo / Analyze"])

# ---------- Welcome Page ----------
if page=="Welcome":
    display_centered_image("welcome_image.jpeg", width=350)
    st.header("👋 Welcome to AI Cyber Safety Teacher")

    welcome_msg = {
        "English":"Welcome to AI Cyber Safety Teacher! Learn how to stay safe online.",
        "Hindi":"AI साइबर सुरक्षा शिक्षक में आपका स्वागत है! ऑनलाइन सुरक्षित रहें।",
        "Kannada":"AI ಸೈಬರ್ ಸೆಕ್ಯುರಿಟಿ ಟೀಚರ್‌ಗೆ ಸ್ವಾಗತ! ಆನ್‌ಲೈನ್ ಸುರಕ್ಷಿತವಾಗಿ ಇರಲು ಕಲಿಯಿರಿ."
    }

    st.write(welcome_msg[lang])
    speak_streamlit(welcome_msg[lang], lang_code=lang_code)

# ---------- Cyber Attack Details ----------
elif page=="Cyber Attack Details":
    display_centered_image("ai_teacher_logo.jpeg", width=250)
    st.header("📌 Cyber Attack Types")

    attack_details = {
        "phishing": "Fake links to steal info",
        "malware": "Harmful software",
        "ransomware": "Locks files for money",
        "social_engineering": "Tricks users",
        "password_attack": "Password stealing",
        "otp_fraud": "OTP scams",
        "lottery_scam": "Fake lottery",
        "fake_app": "Fake apps",
        "financial_fraud": "Money fraud",
        "spyware_adware": "Tracking apps"
    }

    for key, desc in attack_details.items():
        st.write(f"• {key.replace('_',' ').title()}: {desc}")
        speak_streamlit(f"{key.replace('_',' ').title()}: {desc}", lang_code=lang_code)

# ---------- Demo ----------
elif page=="Demo / Analyze":
    display_centered_image("ai_teacher_logo.jpeg", width=250)
    st.header("🔍 Demo / Manual Message Analysis")

    user_input = st.text_area("📩 Enter message / call content", height=150)

    col1,col2 = st.columns(2)
    with col1: check = st.button("🔍 Analyze")
    with col2: clear = st.button("🧹 Clear")

    if clear:
        st.experimental_rerun()

    if check:
        if user_input.strip() == "":
            st.warning("⚠️ Please enter some text")
            speak_streamlit("Please enter some text.", lang_code=lang_code)
        else:
            category = predict_category(user_input)
            feedback = feedback_dict.get(category, {
                "English":"Be cautious",
                "Hindi":"सतर्क रहें",
                "Kannada":"ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"
            })[lang]

            st.error(feedback)
            speak_streamlit(feedback, lang_code=lang_code)
