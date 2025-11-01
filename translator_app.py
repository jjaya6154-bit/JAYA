from flask import Flask, render_template_string, request
from dotenv import load_dotenv
from openai import OpenAI
import os

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get API key safely
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY is missing. Please set it in your .env file or environment variables.")

# ✅ Initialize OpenAI client
client = OpenAI(api_key=api_key)

# ✅ Flask App Setup
app = Flask(__name__)

# ✅ HTML Template
HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Language Translator</title>
  <style>
    body { 
      font-family: Arial, sans-serif; 
      background: #f4f6f8; 
      text-align: center; 
      margin-top: 60px; 
    }
    textarea { 
      width: 70%; 
      height: 120px; 
      padding: 10px; 
      font-size: 16px; 
      border-radius: 8px; 
      border: 1px solid #ccc;
    }
    select, button { 
      padding: 10px; 
      font-size: 16px; 
      margin: 10px; 
      border-radius: 6px;
    }
    button {
      background-color: #007BFF; 
      color: white; 
      border: none;
      cursor: pointer;
    }
    button:hover {
      background-color: #0056b3;
    }
    h2 { color: #333; }
  </style>
</head>
<body>
  <h2>🌍 Language Translator</h2>
  <form method="POST">
    <textarea name="text" placeholder="Enter text to translate..." required></textarea><br>
    <select name="target_lang">
      <option value="Tamil">Tamil</option>
      <option value="Hindi">Hindi</option>
      <option value="French">French</option>
      <option value="Japanese">Japanese</option>
    </select><br>
    <button type="submit">Translate</button>
  </form>

  {% if translated %}
  <h3>🔤 Translated Message:</h3>
  <p>{{ translated }}</p>
  {% elif error %}
  <h3 style="color:red;">⚠️ {{ error }}</h3>
  {% endif %}
</body>
</html>
"""

# ✅ Flask Route
@app.route("/", methods=["GET", "POST"])
def home():
    translated = error = None
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        target_lang = request.form.get("target_lang", "")
        if not text:
            error = "Please enter some text."
        else:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful translation assistant."},
                        {"role": "user", "content": f"Translate this to {target_lang}: {text}"}
                    ]
                )
                translated = response.choices[0].message.content
            except Exception as e:
                error = f"⚠️ Error: {e}"
    return render_template_string(HTML, translated=translated, error=error)


# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
