from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Hugging Face Inference API 정보
API_URL = "https://api-inference.huggingface.co/models/Nudge5/cdci-2-7b"
HEADERS = {"Authorization": "Bearer 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"}

def query_huggingface_api(prompt):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        response.encoding = 'utf-8'
        print("Response content:", response.content)
        print("Response text:", response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error during API call:", e)
        return {"error": "API request failed"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    result = query_huggingface_api(prompt)
    
    if "error" in result:
        return jsonify({"error": result.get("error", "Unknown error occurred.")}), 500
    
    if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
        response_text = result[0]['generated_text']
        answer = response_text.replace(prompt, "").strip()
        return jsonify({"response": answer})
    else:
        return jsonify({"error": "Invalid response structure or no generated text."}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
