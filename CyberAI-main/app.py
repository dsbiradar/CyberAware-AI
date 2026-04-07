# app.py
import streamlit as st
import joblib
import io
from gtts import gTTS
from PIL import Image
import pytesseract
from utils import scenarios  # your original utils import

# ---------- Function to display centered images ----------
def display_centered_image(image_path, width=250):
    try:
        img = Image.open(image_path)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(img, width=width)
    except Exception as e:
        st.warning(f"Image not found or failed to load: {e}")

# ---------- Audio function ----------
def speak_streamlit(text, lang_code="en"):
    tts = gTTS(text=text, lang=lang_code)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp, format="audio/mp3")

# ---------- Load model ----------
model_path = "cyber_model.pkl"
model_loaded = False
try:
    model = joblib.load(model_path)
    model_loaded = True
except Exception as e:
    st.error(f"⚠️ Model not found or error loading: {e}")

def predict_category(text):
    if not model_loaded:
        speak_streamlit("Model not loaded. Cannot predict.", lang_code="en")
        return "unknown"
    return model.predict([text])[0]

# ---------- Feedback dictionary ----------
feedback_dict = {
    "phishing":{"English":"This message contains a suspicious link. Do NOT click it.","Hindi":"इस संदेश में संदिग्ध लिंक है। इसे क्लिक न करें।","Kannada":"ಈ ಸಂದೇಶದಲ್ಲಿ ಅನುಮಾನಾಸ್ಪದ ಲಿಂಕ್ ಇದೆ. ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ."},
    "malware":{"English":"This file or link can harm your phone. Do NOT open it.","Hindi":"यह फ़ाइल या लिंक आपके फोन को नुकसान पहुंचा सकता है। इसे न खोलें।","Kannada":"ಈ ಫೈಲ್ ಅಥವಾ ಲಿಂಕ್ ನಿಮ್ಮ ಫೋನ್‌ಗೆ ಹಾನಿ ಮಾಡಬಹುದು. ತೆರೆಯಬೇಡಿ."},
    "ransomware":{"English":"Your device may be locked for money. Do NOT pay anything.","Hindi":"आपका डिवाइस पैसे के लिए लॉक किया जा सकता है। पैसे न दें।","Kannada":"ನಿಮ್ಮ ಸಾಧನವನ್ನು ಹಣಕ್ಕಾಗಿ ಲಾಕ್ ಮಾಡಬಹುದು. ಹಣ ಕೊಡಬೇಡಿ."},
    "social_engineering":{"English":"Someone is trying to trick you. Do NOT trust easily.","Hindi":"कोई आपको धोखा देने की कोशिश कर रहा है। आसानी से विश्वास न करें।","Kannada":"ಯಾರೋ ನಿಮ್ಮನ್ನು ಮೋಸ ಮಾಡಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದಾರೆ. ಸುಲಭವಾಗಿ ನಂಬಬೇಡಿ."},
    "password_attack":{"English":"Someone is trying to get your password. Keep it safe.","Hindi":"कोई आपका पासवर्ड लेने की कोशिश कर रहा है। इसे सुरक्षित रखें।","Kannada":"ಯಾರೋ ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್ ಪಡೆಯಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದಾರೆ. ಸುರಕ್ಷಿತವಾಗಿರಿಸಿ."},
    "otp_fraud":{"English":"This message is asking for OTP. Do NOT share it.","Hindi":"यह OTP मांग रहा है। साझा न करें।","Kannada":"ಇದು OTP ಕೇಳುತ್ತಿದೆ. ಹಂಚಬೇಡಿ."},
    "lottery_scam":{"English":"Fake lottery messages claiming you won. Ignore them.","Hindi":"आप जीत गए हैं कहने वाले नकली लॉटरी संदेश। इन्हें अनदेखा करें।","Kannada":"ನೀವು ಗೆದ್ದೀರಿ ಎಂದು ಹೇಳುವ ನಕಲಿ ಲಾಟರಿ ಸಂದೇಶಗಳು. ನಿರ್ಲಕ್ಷ್ಯ ಮಾಡಿ."},
    "fake_app":{"English":"This app is not safe. Do not install it.","Hindi":"यह ऐप सुरक्षित नहीं है। इसे इंस्टॉल न करें।","Kannada":"ಈ ಆಪ್ ಸುರಕ್ಷಿತವಲ್ಲ. ಸ್ಥಾಪಿಸಬೇಡಿ."},
    "financial_fraud":{"English":"This message is trying to take your money. Be alert.","Hindi":"यह संदेश आपके पैसे लेने की कोशिश कर रहा है। सावधान रहें।","Kannada":"ಈ ಸಂದೇಶ ನಿಮ್ಮ ಹಣ ತೆಗೆದುಕೊಳ್ಳಲು ಪ್ರಯತ್ನಿಸುತ್ತದೆ. ಎಚ್ಚರಿಕೆ ವಹಿಸಿ."},
    "spyware_adware":{"English":"This may track your phone activity secretly. Be careful.","Hindi":"यह आपके फोन को गुप्त रूप से ट्रैक कर सकता है। सावधान रहें।","Kannada":"ಇದು ನಿಮ್ಮ ಫೋನ್ ಚಟುವಟಿಕೆಯನ್ನು ಗುಪ್ತವಾಗಿ ಟ್ರಾಕ್ ಮಾಡಬಹುದು. ಎಚ್ಚರಿಕೆ ವಹಿಸಿ."}
}

# ---------- Navigation ----------
st.sidebar.header("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Welcome","Cyber Attack Details","Demo / Analyze"])

# ---------- Welcome Page ----------
if page=="Welcome":
    display_centered_image("welcome_image.jpeg", width=350)

    lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
    lang_map_code = {"English":"en","Hindi":"hi","Kannada":"kn"}
    lang_code = lang_map_code[lang]

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

    lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
    lang_map_code = {"English":"en","Hindi":"hi","Kannada":"kn"}
    lang_code = lang_map_code[lang]

    st.header("📌 Cyber Attack Types")

    attack_details = {
        "phishing": {"English": "Messages trying to steal your passwords or personal info via fake links.",
                     "Hindi": "संदेश जो आपके पासवर्ड या व्यक्तिगत जानकारी को नकली लिंक के माध्यम से चुराने की कोशिश करते हैं।",
                     "Kannada": "ತಪ್ಪು ಲಿಂಕ್ ಮೂಲಕ ನಿಮ್ಮ ಪಾಸ್ವರ್ಡ್ ಅಥವಾ ವೈಯಕ್ತಿಕ ಮಾಹಿತಿಯನ್ನು ಕದಿಯಲು ಪ್ರಯತ್ನಿಸುವ ಸಂದೇಶಗಳು."},
        "malware": {"English": "Software that harms your device or steals data.",
                    "Hindi": "सॉफ़्टवेयर जो आपके डिवाइस को नुकसान पहुंचाता है या डेटा चुराता है।",
                    "Kannada": "ನಿಮ್ಮ ಸಾಧನಕ್ಕೆ ಹಾನಿ ಮಾಡುವ ಅಥವಾ ಡೇಟಾವನ್ನು ಕದಿಯುವ ಸಾಫ್ಟ್‌ವೇರ್."},
        "ransomware": {"English": "Software that locks your files and demands money to unlock.",
                       "Hindi": "सॉफ़्टवेयर जो आपकी फ़ाइलों को लॉक करता है और उन्हें अनलॉक करने के लिए पैसे मांगता है।",
                       "Kannada": "ನಿಮ್ಮ ಫೈಲ್‌ಗಳನ್ನು ಲಾಕ್ ಮಾಡುವ ಮತ್ತು ಅನ್ಲಾಕ್ ಮಾಡಲು ಹಣ ಕೇಳುವ ಸಾಫ್ಟ್‌ವೇರ್."},
        "social_engineering": {"English": "Tricks to manipulate you into revealing confidential information.",
                               "Hindi": "आपसे गोपनीय जानकारी निकालने के लिए किया गया छल।",
                               "Kannada": "ನಿಮ್ಮ ರಹಸ್ಯ ಮಾಹಿತಿಯನ್ನು ತಿಳಿಸಲು ಮಾಡುವ ಚತುರಾಟ."},
        "password_attack": {"English": "Attempts to guess or steal your passwords.",
                            "Hindi": "आपके पासवर्ड को अनुमान लगाने या चोरी करने का प्रयास।",
                            "Kannada": "ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್ ಅನ್ನು ಊಹಿಸಲು ಅಥವಾ ಕದ್ದಲು ಪ್ರಯತ್ನ."},
        "otp_fraud": {"English": "Fraudulent messages asking for your OTP. Never share it.",
                      "Hindi": "OTP मांगने वाले धोखाधड़ी संदेश। इसे कभी साझा न करें।",
                      "Kannada": "ನಕಲಿ ಸಂದೇಶಗಳು OTP ಕೇಳುತ್ತವೆ. ಹಂಚಬೇಡಿ."},
        "lottery_scam": {"English": "Fake lottery messages claiming you won. Ignore them.",
                         "Hindi": "आप जीत गए हैं कहने वाले नकली लॉटरी संदेश। इन्हें अनदेखा करें।",
                         "Kannada": "ನೀವು ಗೆದ್ದೀರಿ ಎಂದು ಹೇಳುವ ನಕಲಿ ಲಾಟರಿ ಸಂದೇಶಗಳು. ನಿರ್ಲಕ್ಷ್ಯ ಮಾಡಿ."},
        "fake_app": {"English": "Fake apps that may steal data or harm your phone. Do not install.",
                     "Hindi": "नकली ऐप्स जो डेटा चुरा सकते हैं या फोन को नुकसान पहुँचा सकते हैं। इंस्टॉल न करें।",
                     "Kannada": "ನಕಲಿ ಆಪ್‌ಗಳು ನಿಮ್ಮ ಡೇಟಾ ಕದಿಯಬಹುದು ಅಥವಾ ಫೋನ್‌ಗೆ ಹಾನಿ ಮಾಡಬಹುದು. ಸ್ಥಾಪಿಸಬೇಡಿ."},
        "financial_fraud": {"English": "Attempts to steal your money or financial info.",
                            "Hindi": "आपके पैसे या वित्तीय जानकारी को चोरी करने का प्रयास।",
                            "Kannada": "ನಿಮ್ಮ ಹಣ ಅಥವಾ ಹಣಕಾಸು ಮಾಹಿತಿಯನ್ನು ಕದಿಯಲು ಪ್ರಯತ್ನ."},
        "spyware_adware": {"English": "Software that secretly tracks your phone activity or shows unwanted ads.",
                           "Hindi": "सॉफ़्टवेयर जो गुप्त रूप से आपके फ़ोन की गतिविधियों को ट्रैक करता है या अनचाहे विज्ञापन दिखाता है।",
                           "Kannada": "ಸಾಫ್ಟ್‌ವೇರ್ ಇದು ಗುಪ್ತವಾಗಿ ನಿಮ್ಮ ಫೋನ್ ಚಟುವಟಿಕೆಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡುತ್ತದೆ ಅಥವಾ ಅನಗತ್ಯ ಜಾಹೀರಾತು ತೋರಿಸುತ್ತದೆ."}
    }

    for key, desc_dict in attack_details.items():
        st.write(f"• {key.replace('_',' ').title()}: {desc_dict[lang]}")
        speak_streamlit(desc_dict[lang], lang_code=lang_code)

# ---------- Demo / Analyze ----------
elif page=="Demo / Analyze":
    display_centered_image("ai_teacher_logo.jpeg", width=250)

    lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
    lang_map_code = {"English":"en","Hindi":"hi","Kannada":"kn"}
    lang_code = lang_map_code[lang]

    st.header("🔍 Demo / Manual Message Analysis")

    # Text input
    user_input = st.text_area("📩 Enter message / call content", height=150)

    # Screenshot upload
    uploaded_file = st.file_uploader("📷 Upload screenshot (WhatsApp / Email)", type=["png","jpg","jpeg"])
    extracted_text = ""
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Screenshot")
        try:
            extracted_text = pytesseract.image_to_string(image)
            st.write("📄 Extracted text:", extracted_text)
        except Exception as e:
            st.warning(f"Failed to extract text: {e}")

    col1, col2 = st.columns(2)
    with col1:
        check = st.button("🔍 Analyze")
    with col2:
        clear = st.button("🧹 Clear")

    if clear:
        st.experimental_rerun()

    if check:
        # Use text area if present, otherwise OCR text
        final_text = user_input if user_input.strip() != "" else extracted_text

        if final_text.strip() == "":
            st.warning("⚠️ Please enter some text")
            speak_streamlit("Please enter some text to analyze.", lang_code=lang_code)
        else:
            category = predict_category(final_text)
            feedback = feedback_dict.get(
                category,
                {"English":"Be cautious","Hindi":"सतर्क रहें","Kannada":"ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"}
            )[lang]

            st.error(feedback)
            # Speak only the description in selected language
            speak_streamlit(feedback, lang_code=lang_code)
