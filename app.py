import os
import logging

import openai
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


logger = logging.getLogger(__name__)


@app.route("/gen_plan", methods=("GET", "POST"))
def generate_plan():
    # TODO: add try-catch for KeyError
    if request.method == "POST":
        task = 'Week: 1; suggested day to post: Monday; suggested length: 550; format: how-to post; suggested heading:'
        form = request.get_json()
        profession = form["profession"]
        experience = form["experience"]
        length = form.get("n", 5)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_gen_plan(profession=profession, experience=experience, task=task, n=length),
            temperature=0.6,
            max_tokens=3100,
        )
        print(f'OpenAI response: {response.choices}')
        return jsonify({"response": f'{task} {response.choices[0].text}'})
    return abort(403, "GET method is not allowed")

def prompt_gen_plan(profession, experience, task, n=5):
    return f"""Brief review of my LinkedIn profile: I am {profession}.
My experience: {experience}.
You will create a content plan (headings only) for my LinkedIn blog.
Suggest {n} LinkedIn post topics based on my profession and background, do not use companies I worked for, use different formats.

{task}
"""


@app.route("/gen_post", methods=("GET", "POST"))
def generate_post():
    # TODO: add try-catch for KeyError
    if request.method == "POST":
        form = request.get_json()
        profession = form["profession"]
        experience = form["experience"]
        topic = form["topic"]
        length = form["length"]
        post_format = form["post_format"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_gen_post(
                profession=profession,
                experience=experience,
                topic=topic,
                length=length,
                post_format=post_format,
            ),
            max_tokens=3100,
            temperature=0.6,
        )
        return jsonify({"response": response.choices[0].text})
    return abort(403, "GET method is not allowed")

def prompt_gen_post(profession, experience, topic, length, post_format):
    return f"""Brief review of my LinkedIn profile: I am {profession}.
My experience: {experience}.
Generate a post for my LinkedIn blog, topic: "{topic}", desired length: {length}, desired format: {post_format}.
Only heading and body. The length must be {length}, pay attention to format.
"""

@app.route("/gen_image", methods=("GET", "POST"))
def generate_image():
    # TODO: add try-catch for KeyError
    if request.method == "POST":
        form = request.get_json()
        topic = form["topic"]
        response = openai.Image.create(
            prompt=f"Illustration for linkedin post: '{topic}'",
            n=1,
            size="1024x1024"
        )
        return jsonify({"response": response['data'][0]['url']})
    return abort(403, "GET method is not allowed")
