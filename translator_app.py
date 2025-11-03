import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# ✅ Load environment variables first
load_dotenv()

# ✅ Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# App title
st.set_page_config(page_title="🌍 Language Translator", page_icon="🌍")
st.title("🌍 Language Translator")

# User input
text = st.text_area("Enter text to translate:", height=150)

# Language selection
target_lang = st.selectbox(
    "Choose target language:",
    ["Tamil", "Hindi", "French", "Japanese"]
)

if st.button("Translate"):
    if text.strip() == "":
        st.warning("⚠️ Please enter some text first!")
    else:
        try:
            with st.spinner("Translating..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful translation assistant."},
                        {"role": "user", "content": f"Translate this to {target_lang}: {text}"}
                    ]
                )
                translated = response.choices[0].message.content
                st.success("✅ Translation complete!")
                st.write("### 🔤 Translated Text:")
                st.write(translated)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
