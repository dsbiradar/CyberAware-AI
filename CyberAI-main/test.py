# test.py
import joblib

# Load trained model
model = joblib.load("cyber_model.pkl")

# Sample messages
test_samples = {
    "phishing": "Click this suspicious link to claim prize",
    "malware": "Install this app to get reward",
    "ransomware": "Your files locked, pay to unlock",
    "social_engineering": "Call asking OTP for verification",
    "password_attack": "Someone asking for password",
    "otp_fraud": "Someone asked my OTP",
    "lottery_scam": "You won a lottery you never entered",
    "fake_app": "Install this fake banking app",
    "financial_fraud": "Bank transfer requested from unknown",
    "spyware_adware": "App is secretly tracking your device"
}

correct_count = 0
for cat, msg in test_samples.items():
    pred = model.predict([msg])[0]
    result = "✅ Correct" if pred==cat else f"❌ Wrong (Predicted: {pred})"
    print(f"Category: {cat} | Message: '{msg}' | Result: {result}")
    if pred==cat: correct_count += 1

print(f"\nOverall Accuracy on Sample Test Messages: {correct_count}/{len(test_samples)}")
