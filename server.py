import json
from flask import Flask
from flask import request
from flask import jsonify




app = Flask(__name__)


@app.route('/', methods=["POST"])
def add():
    count = 0
    data_new = request.get_json(force=False)
    with open('json/game_data.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    for i in data_new:
        if data.get(i) == None or len(data_new[i]["photo"]) > len(data[i]["photo"]):
            data[i] = data_new[i]
            count += 1

    with open('json/game_data.json', 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(data,indent=2,ensure_ascii=False))

    return "Words added to the database: {0}".format(count)


@app.route("/", methods=["GET"])
def get():
    data_re = request.args

    if not data_re:
        data_re = {}

    with open('json/game_data.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    if int(data_re.get("json")):
        return jsonify(data)

    text = "Количество слов: {0}.<br>Количество картинок: {1}<br>Слова:<br>".format(len(data),sum([len(data[i]["photo"]) for i in data]))
    for i in data:
        text += "{0} : {1}.<br>".format(i, len(data[i]["photo"]))

    return text


@app.route("/", methods=["DELETE"])
def delete():
    with open('json/game_data.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    count = 0
    for i in data:
        if len(data[i]["photo"]) == 0 or len(data[i]["resize_photo"]) == 0:
            del data[i]
            count += 1
    with open('json/game_data.json', 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(data,indent=2,ensure_ascii=False))

    return "Removed words from the database: {0}.".format(count)


app.run(host="0.0.0.0",port=5555)
