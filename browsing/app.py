import os
import json
from flask import Flask, request, render_template

app = Flask(__name__, template_folder = "template", static_folder = "static")

def absPath(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

def writeNote(data):
    if (os.path.isfile(absPath("../notes.csv"))):
        mode = "a"
        prefix = ""
    else:
        mode = "w"
        prefix = "sep=|\ndate|title|note|url|keywords\n"

    with open(absPath("../notes.csv"), mode) as f:
        f.write(f"{prefix}{data['date']}|{data['title']}|{data['note']}|{data['url']}|{data['keywords']}\n")


@app.route("/", methods = ["GET", "POST"])
def index():
    if (request.method == "GET"):
        paperFiles = enumerate(sorted(os.listdir(absPath("../results")), reverse = True))
        return render_template("browsing.html", paperFiles = paperFiles)
    elif (request.method == "POST"):
        data = request.json

        if (data["task"] == "selectFile"):
            with open(absPath(f"../results/{data['fileName']}"), "r") as f:
                returnData = json.load(f)
        elif (data["task"] == "writeNotes"):
            writeNote(data)
            returnData = {}
        
        return returnData


if (__name__ == "__main__"):
    app.run(host = "127.0.0.1", debug = True)