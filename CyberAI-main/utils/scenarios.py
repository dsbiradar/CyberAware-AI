# utils/scenarios.py

scenarios = [
    {"scenario":"Someone called asking for OTP","answer":"no","explanation":"Never share OTP with anyone."},
    {"scenario":"Email asking to reset password via link","answer":"no","explanation":"Check official source, phishing alert."},
    {"scenario":"Bank calls asking account number to verify","answer":"no","explanation":"Banks never ask sensitive info on call."},
    {"scenario":"Download free antivirus from unknown site","answer":"no","explanation":"Could be malware."},
    {"scenario":"Received message claiming lottery win","answer":"no","explanation":"Most lottery messages are scams."},
    {"scenario":"Someone asking for your PIN to help","answer":"no","explanation":"Never share PIN with anyone."},
    {"scenario":"App requests camera & mic access unnecessarily","answer":"no","explanation":"Check app legitimacy before granting."},
    {"scenario":"Unknown link promising free gift","answer":"no","explanation":"Could be phishing."},
    {"scenario":"Software update prompt from official website","answer":"yes","explanation":"Legitimate updates are safe."},
    {"scenario":"Trusted bank app requests login to view balance","answer":"yes","explanation":"Official apps are safe."}
]
