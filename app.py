import os
import requests
from flask_cors import CORS
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def main():
    return "Ok"

@app.route("/webhook", methods=["POST"])
def router():
    data = request.json

    api_url = "https://envapi-ogviuwianebse-app-service.azurewebsites.net/api/v2"
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    if not email or not password:
        return "No email or password found."

    login_data = {
        "email": email,
        "password": password
    }

    session = requests.Session()
    login_response = session.post(
        f"{api_url}/login/",
        json=login_data
    )

    if login_response.status_code == 200:
        print("Authorized for sending data...")
    else:
        print("Not authorized for sending data.", login_response.status_code, login_response.text)
        return "Not authorized for sending data."

    labels = session.get(f"{api_url}/label/")
    labels = labels.json()["data"]

    shipment_id = next(
        (item["shipment_id"] for item in labels if item["label_response"]["response"]["identifier"] == data["identifier"]),
        None
    )
    if shipment_id:
        print("Shipment ID encontrado en labels desde el identifier de beetrack.")
    else:
        print("Identifier no encontrado.")
        return "Identifier no encontrado."

    shipment = session.get(f"{api_url}/shipment/{shipment_id}")
    if shipment.status_code == 200:
        print ("Shipment encontrado")
    else:
        print("Shipment no encontrado.")
        return "Shipment no encontrado."
    business_id = shipment.json()["data"]["business_id"]

    business = session.get(f"{api_url}/business/{business_id}")
    if business.status_code == 200:
        print ("Business encontrado")
    else:
        print("Business no encontrado.")
        return "Business no encontrado."
    business_code = business.json()["data"]["business_code"]

    print(f"Business code: {business_code}")

    if business_code == "1": # Xiaomi
        requests.post("https://mistoremx.com/etiqueta.php", json=data)
        print("Data success sent for Xiaomi")
        return "Data success sent for Xiaomi"
    elif business_code == "2": # Doto
        requests.post(
            "https://sandboxshipmentsapi.doto.com.mx/api/v1/webhooks/enviadero/tracker", json=data)
        requests.post(
            "https://shipmentsapi.doto.com.mx/api/v1/webhooks/enviadero/tracker", json=data)
        print("Data success sent for Doto")
        return "Data success sent for Doto"
    elif business_code == "dichipet":
        print("Data success sent for Dichipet")
        return "Data success sent for Dichipet"
    elif business_code == "mainbit":
        print("Data success sent for Mainbit")
        return "Data success sent for Mainbit"
    elif business_code == "serge":
        print("Data success sent for Serge")
        return "Data success sent for Serge"
    elif business_code == "sago":
        print("Data success sent for Sago")
        return "Data success sent for Sago"
    elif business_code == "totto":
        print("Data success sent for Totto")
        return "Data success sent for Totto"
    elif business_code == "kubo financiero":
        print("Data success sent for Kubo financiero")
        return "Data success sent for Kubo financiero"
    elif business_code == "helgen":
        print("Data success sent for Helgen")
        return "Data success sent for Helgen"
    elif business_code == "data components":
        print("Data success sent for Data components")
        return "Data success sent for Data components"
    else:
        print("Business not found")
        return "Business not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000", debug=True)
