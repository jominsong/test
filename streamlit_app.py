$install openai flask

from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = "sk"  # 여기에 본인의 키 입력

@app.route("/", methods=["GET", "POST"])
def chat():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["user_input"]

        # GPT-4.1-mini 모델 호출
        completion = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 AI입니다."},
                {"role": "user", "content": user_input}
            ]
        )
        response_text = completion.choices[0].message["content"]

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)

<!DOCTYPE html>
<html>
<head>
  <title>GPT-4.1-mini 웹 챗봇</title>
</head>
<body>
  <h2>GPT-4.1-mini에 질문해보세요</h2>
  <form method="POST">
    <input type="text" name="user_input" style="width:300px;" placeholder="질문을 입력하세요" required>
    <button type="submit">보내기</button>
  </form>
  {% if response %}
    <h3>GPT 응답:</h3>
    <p>{{ response }}</p>
  {% endif %}
</body>
</html>
