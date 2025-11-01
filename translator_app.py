from flask import Flask, render_template_string, request
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Language Translator</title>
  <style>
    body { font-family: Arial; background: #f4f6f8; text-align: center; margin-top: 60px; }
    textarea { width: 70%; height: 120px; padding: 10px; font-size: 16px; }
    select, button { padding: 10px; font-size: 16px; margin: 10px; }
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

@app.route("/", methods=["GET", "POST"])
def home():
    translated = error = None
    if request.method == "POST":
        text = request.form["text"]
        target_lang = request.form["target_lang"]
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
            error = f"Error: {str(e)}"
    return render_template_string(HTML, translated=translated, error=error)

if __name__ == "__main__":
    app.run(debug=True)
