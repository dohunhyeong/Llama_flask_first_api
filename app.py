from flask import Flask, request, jsonify, render_template
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel

app = Flask(__name__)

# 모델 로드
base_model_name = "winglian/Llama-2-3b-hf"
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
base_model = AutoModelForCausalLM.from_pretrained(base_model_name, torch_dtype=torch.float16)

# LoRA 모델 로드 및 적용
lora_model_path = "models"  # 로컬 경로로 변경 필요
model = PeftModel.from_pretrained(base_model, lora_model_path)

# 파이프라인 설정
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=200, device=-1)  # GPU 사용

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # 요청에서 질문 가져오기
    data = request.json
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    # 모델에 질문 입력
    result = pipe(f'<s>[INST] {prompt}[/INST]')
    
    # 결과 반환
    return jsonify({"response": result[0]['generated_text']})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)
    
