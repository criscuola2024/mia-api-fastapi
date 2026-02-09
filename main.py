from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import json
import gspread
from google.oauth2.service_account import Credentials

app = FastAPI()

# ==========================
# GOOGLE SHEETS SETUP
# ==========================

# Carica la service account key dalla variabile d’ambiente
service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])

creds = Credentials.from_service_account_info(
    service_account_info,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)


client = gspread.authorize(creds)

# Nome del foglio Google
SHEET_NAME = "studenti_api"
sheet = client.open(SHEET_NAME).sheet1


# ==========================
# FUNZIONI DI SUPPORTO
# ==========================

def load_db():
    """Legge tutte le righe del foglio e le restituisce come lista di dict."""
    return sheet.get_all_records()


def save_row(row):
    """Aggiunge una nuova riga al foglio."""
    sheet.append_row(row)


def update_row(row_index, row_values):
    """Aggiorna una riga esistente (senza toccare l'header)."""
    # row_index parte da 2 perché la riga 1 è l’header
    sheet.update(f"A{row_index}:Z{row_index}", [row_values])


def delete_row(row_index):
    """Cancella una riga dal foglio."""
    sheet.delete_rows(row_index)


# ==========================
# ENDPOINTS API
# ==========================

@app.get("/studenti")
def get_studenti():
    data = load_db()
    return JSONResponse(content=data)


@app.get("/studenti/{id}")
def get_studente(id: int):
    data = load_db()
    for studente in data:
        if studente["id"] == id:
            return JSONResponse(content=studente)
    return JSONResponse(content={"error": "Studente non trovato"}, status_code=404)


@app.post("/studenti")
def add_studente(studente: dict):
    data = load_db()

    nuovo_id = len(data) + 1
    studente["id"] = nuovo_id

    # Ordine delle colonne come nel foglio
    row = [studente.get("id"), studente.get("nome"), studente.get("cognome"), studente.get("classe")]

    save_row(row)

    return JSONResponse(content=studente, status_code=201)


@app.put("/studenti/{id}")
def update_studente(id: int, studente: dict):
    data = load_db()

    for index, s in enumerate(data, start=2):  # start=2 perché riga 1 è header
        if s["id"] == id:
            # aggiorna i valori
            s.update(studente)

            row_values = [s.get("id"), s.get("nome"), s.get("cognome"), s.get("classe")]
            update_row(index, row_values)

            return JSONResponse(content=s)

    return JSONResponse(content={"error": "Studente non trovato"}, status_code=404)


@app.delete("/studenti/{id}")
def delete_studente(id: int):
    data = load_db()

    for index, s in enumerate(data, start=2):
        if s["id"] == id:
            delete_row(index)
            return {"deleted": id}

    return JSONResponse(content={"error": "Studente non trovato"}, status_code=404)


