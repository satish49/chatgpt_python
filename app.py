import os
import re
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        query = request.form["query"]

        response = openai.Completion.create(
            prompt=query,
            top_p=1,
            model="text-davinci-003",
            temperature=0.7,
            max_tokens=2066,
            frequency_penalty=0,
            presence_penalty=0

        )
        print("response")
        print(response)
        textData = response.choices[0].text
        print("textData")
        print(textData)
        print(type(textData))
        # Replace '%0A' with newlines and '+' with spaces
        textData = re.sub(r'%0A', '\n', textData)
        textData = re.sub(r'\+', ' ', textData)

        # Split the string into lines
        lines = textData.split('\n')
        print("type of lines "+str(type(lines)))
        for line in lines:
            print(line)

        print(response.usage)

        return render_template("index.html", results = textData, tokensInfo= response.usage)

    result = request.args.get("results")
    return render_template("index.html", results=result)


@app.route("/generate", methods=["POST"])
def generate():
    print("in generate")
    print("query")
    print(request.get_json())
    query = request.get_json()["query"]

    print("calling OpenAI with Query")
    response = openai.Completion.create(
        prompt=query,
        top_p=1,
        model="text-davinci-003",
        temperature=0.7,
        max_tokens=3066,
        frequency_penalty=0,
        presence_penalty=0

    )
    print("response from OpenAI")
    print(response)
    print("read response data using choices[0]")
    textData = response.choices[0].text
    print("textData")
    print(textData)
    print(type(textData))
    # Replace '%0A' with newlines and '+' with spaces
    textData = re.sub(r'%0A', '\n', textData)
    textData = re.sub(r'\+', ' ', textData)

    # Split the string into lines
    lines = textData.split('\n')
    print("type of lines "+str(type(lines)))
    for line in lines:
        print(line)

    print(response.usage)
    print("end of generate API")
    return {"data":response.choices[0].text, "tokens": response.usage}
    
@app.route("/hello", methods=["GET"])
def hello():
    print("in hello api")
    return "Hi"