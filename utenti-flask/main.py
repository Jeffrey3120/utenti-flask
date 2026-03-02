from flask import Flask, request
import uuid
from faker import Faker

app = Flask(__name__)
fake = Faker()

users = []

# genera utenti fake
for _ in range(5):
    user = {
        "id": str(uuid.uuid4()),
        "nome": fake.first_name(),
        "cognome": fake.last_name(),
        "email": fake.email(),
        "citta": fake.city(),
        "data_nascita": fake.date_of_birth().isoformat()
    }
    users.append(user)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# GET tutti
@app.route("/api/user", methods=["GET"])
def get_user():
    return users

# GET singolo
@app.get("/api/user/<user_id>")
def get_user_singolo(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"errore": "Utente non trovato"}, 404

# POST
@app.route("/api/user", methods=["POST"])
def create_user():
    data = request.get_json() or {}

    nuovo = {
        "id": str(uuid.uuid4()),  
        "nome": data.get("nome", fake.first_name()),
        "cognome": data.get("cognome", fake.last_name()),
        "email": data.get("email", fake.email()),
        "citta": data.get("citta", fake.city()),
        "data_nascita": data.get("data_nascita", fake.date_of_birth().isoformat())
    }

    users.append(nuovo)
    return nuovo, 201

# PUT
@app.route("/api/user/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json() or {}

    for user in users:
        if user["id"] == user_id:
            user["nome"] = data.get("nome", user["nome"])
            user["cognome"] = data.get("cognome", user["cognome"])
            user["email"] = data.get("email", user["email"])
            user["citta"] = data.get("citta", user["citta"])
            user["data_nascita"] = data.get("data_nascita", user["data_nascita"])
            return user

    return {"errore": "Utente non trovato"}, 404

# DELETE singolo
@app.route("/api/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return {"messaggio": "Utente eliminato"}, 200
    return {"errore": "Nessun utente trovato"}, 404

# DELETE tutti
@app.route("/api/user", methods=["DELETE"])
def delete_all_user():
    users.clear()
    return {"messaggio": "Tutti gli utenti eliminati"}, 200

if __name__ == "__main__":
    app.run("0.0.0.0", 11000, debug=True)