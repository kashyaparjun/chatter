from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
import jsoner
import os

app = Flask(__name__)

chatbot = ChatBot(
    'Bot01',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.5,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    response_selection_method=get_random_response,
    tie_breaking_method="random_response"
)

from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot.set_trainer(ChatterBotCorpusTrainer)
temp = [
    "./data/trailer.json"
]
chatbot.train(temp)
chatbot.read_only = True

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

@app.route("/getAll")
def get_all():
    return str(jsoner.readFile())

@app.route("/writeChange", methods=['GET', 'POST'])
def changer():
    chatbot.storage.drop()
    chatbot.storage_adapter = 'chatterbot.storage.SQLStorageAdapter'
    ques = request.json
    print(ques)
    jsoner.writeFile(ques)
    chatbot.train(temp)
    return "okay"


if __name__ == "__main__":
    app.run()
