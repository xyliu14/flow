from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv 

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input_chinese = request.form["chinese"]
    user_input_english = request.form["english"]
    prompt = f"This is the target expression in Chinese: {user_input_chinese}. This is an English expression for assessment: {user_input_english}. Assess the naturalness of this English expression using a percentage score. If this is less commonly used among native speakers, give three examples to express this idea like a local, and say no more."
    chat_history = []
    response = openai.chat.completions.create(
        model= "gpt-3.5-turbo",
        messages=[
            {
                "role": "system", "content": "You are a teacher of English who teaches Chinese students."
            },
            {
                "role": "user", "content": (prompt)
            }
        ],
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        stop=["\nUser: ", "\nChatbot: "]
    )

    bot_response = response.choices[0].message.content

    chat_history.append(f"Chinese: {user_input_chinese}\nEnglish: {user_input_english}\nChatbot: {bot_response}")

    return render_template(
        "chatbot.html",
        user_input_chinese=user_input_chinese,
        user_input_english=user_input_english,
        bot_response=bot_response 
    )

if __name__ == '__main__':
    app.run(debug=True)