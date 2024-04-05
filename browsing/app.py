import os
import json
from flask import Flask, request, render_template

app = Flask(__name__, template_folder = "template", static_folder = "static")

def absPath(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

def getPrevNotes(data):
    if (not os.path.isfile(absPath("../notes.csv"))): return ""

    with open(absPath("../notes.csv"), "r") as f:
        for l in f.readlines():
            if (data["url"] in l):
                return l.split("|")[2]
    
    return ""


def writeNote(data):
    if ((data["note"] == "") or (data["note"] == None)): return

    if (os.path.isfile(absPath("../notes.csv"))):
        seek = 0
        remainLines = ""

        with open(absPath("../notes.csv"), "r+") as f:
            find = False

            for l in f.readlines():
                if (data["url"] in l):
                    find = True
                elif (not find):
                    seek += len(l)
                else:
                    remainLines += l
        
            f.seek(seek, 0)
            f.write(f"{data['date']}|{data['title']}|{data['note']}|{data['url']}|{data['keywords']}\n{remainLines}")

            if (remainLines != ""):
                f.truncate()
    else:
        with open(absPath("../notes.csv"), "w") as f:
            prefix = "sep=|\ndate|title|note|url|keywords\n"
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
        elif (data["task"] == "pre-writeNotes"):
            prevNotes = getPrevNotes(data)
            returnData = {"prevNotes": prevNotes}
        elif (data["task"] == "writeNotes"):
            writeNote(data)
            returnData = {}
        
        return returnData


if (__name__ == "__main__"):
    app.run(host = "127.0.0.1", debug = True)