from fastapi import FastAPI
import json
import os
import requests
import base64



app = FastAPI()
DB_FILE = "db.json"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
'''def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)
    with open(DB_FILE, "r") as f:
        return json.load(f)'''

def load_db():
    url = "https://api.github.com/repos/criscuola2024/mia-api-fastapi/contents/db.json"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    r = requests.get(url, headers=headers)
    content = r.json()

    file_content = base64.b64decode(content["content"]).decode("utf-8")
    data = json.loads(file_content)

    return data, content["sha"]


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/studenti")
def get_studenti():
    return load_db()

@app.get("/studenti/{id}")
def get_studenti(id: int):
    data=load_db()
    studente=data[id]
    return studente
    
@app.route("/studenti", methods=["POST"])
def add_studente():
    data, sha = load_db()
    nuovo = request.get_json()

    nuovo["id"] = len(data) + 1
    data.append(nuovo)

    save_db(data, sha)

    return jsonify(nuovo), 201

'''
@app.put("/studenti/{id}")
def update_studente(id: int, studente: dict):
    data = load_db()
    for s in data:
        if s["id"] == id:
            s.update(studente)
            save_db(data)
            return s
    return {"error": "not found"}

@app.delete("/studenti/{id}")
def delete_studente(id: int):
    data = load_db()
    data = [s for s in data if s["id"] != id]
    save_db(data)
    return {"deleted": id}'''





