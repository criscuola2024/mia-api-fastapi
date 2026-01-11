from fastapi import FastAPI
import json
import os

app = FastAPI()
DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/studenti")
def get_studenti():
    return load_db()

@app.post("/studenti")
def add_studente(studente: dict):
    data = load_db()
    studente["id"] = len(data) + 1
    data.append(studente)
    save_db(data)
    return studente

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
    return {"deleted": id}
