import streamlit as st
import re

def check_strength(password):
    score = 0

    # Conditions
    length = len(password) >= 8
    lower = re.search(r"[a-z]", password)
    upper = re.search(r"[A-Z]", password)
    digit = re.search(r"\d", password)
    special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

    # Scoring
    if length: score += 1
    if lower: score += 1
    if upper: score += 1
    if digit: score += 1
    if special: score += 1

    # Result
    if score <= 2:
        return "Weak", score
    elif score == 3 or score == 4:
        return "Moderate", score
    else:
        return "Strong", score

# Streamlit UI
st.title("🔐 Password Strength Checker")

password = st.text_input("Enter your password", type="password")

if password:
    strength, score = check_strength(password)
    st.write(f"**Strength:** {strength}")

    st.progress(score * 20)

    # Tips
    if strength == "Weak":
        st.warning("Tip: Use a mix of uppercase, lowercase, numbers, and special characters. Minimum length: 8")
    elif strength == "Moderate":
        st.info("Tip: Add more complexity or increase password length.")
    else:
        st.success("Great! Your password is strong.")
