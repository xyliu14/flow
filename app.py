from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv 

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)

@app.route("/", methods=['POST'])
def home():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    user_input_chinese = request.form["chinese"]
    user_input_english = request.form["english"]
    prompt = f"""This is the Chinese context: {user_input_chinese}. This is an English expression based on the Chinese context to be assessed: {user_input_english}. 
                Rate the expression from:
                \"Natural (commonly used by native speakers; only give this rating if a native speaker of English would say this exact expression)\", 
                \"Understandable (not often used by native speakers but understandable)\", to 
                \"Questionnable (hard to understand)\". 
                Return a list with four elements, no explanations, no tags: rating of this expression and three examples of the native equivalent.
                
                Example: 
                Questionable, Affordable price, Budget-friendly price, Reasonable price
                """
    response = openai.chat.completions.create(
        model= "gpt-4o",
        messages=[
            {
                "role": "system", "content": "You are a teacher of English who teaches Chinese students how to speak like a native speaker."
            },
            {
                "role": "user", "content": (prompt)
            }
        ],
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
    )

    bot_response = response.choices[0].message.content
    response_parts = bot_response.split(', ')

    return render_template(
        "results.html",
        user_input_chinese=user_input_chinese,
        user_input_english=user_input_english,
        evaluation_result=response_parts[0], 
        expression_1=response_parts[1] if len(response_parts) > 1 else "", 
        expression_2=response_parts[2] if len(response_parts) > 2 else "",
        expression_3=response_parts[3] if len(response_parts) > 3 else "" 
    )

if __name__ == '__main__':
    app.run(debug=True)