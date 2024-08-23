from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Hugging Face Inference API 정보
API_URL = "https://rpvt8ykj2p7hzz02.us-east-1.aws.endpoints.huggingface.cloud"
HEADERS = {"Authorization": "Bearer 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"}

def query_huggingface_api(prompt):
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {
            "max_length": 700,
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.9,
            "do_sample": True
        }
    }    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return {"error": "API request failed with status code " + str(response.status_code)}

        result = response.json()

        # 후처리 단계: 스페셜 토큰 및 태그 제거
        if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
            generated_text = result[0]['generated_text']
            cleaned_text = generated_text.replace("[INST]", "").replace("[/INST]", "").replace("<s>", "").replace("</s>", "").strip()
            
            # 질문 부분 제거
            if prompt in cleaned_text:
                cleaned_text = cleaned_text.replace(prompt, "").strip()

            return {"generated_text": cleaned_text}
        else:
            return {"error": "Invalid response structure or no generated text."}
    except requests.exceptions.RequestException as e:
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
    
    # Query 함수에서 이미 처리된 결과를 그대로 반환
    return jsonify({"response": result.get('generated_text', "Unknown error occurred.")})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
