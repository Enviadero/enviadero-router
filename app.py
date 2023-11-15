from flask import Flask, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def main():
    return "Ok"

@app.route('/webhook', methods=['POST'])
def router():
    data = request.json
    print(data)

    business = requests.get("https://tim-loonie-94123.herokuapp.com/business")

    labels = {}
    business_code = None

    for item in business.json():
        labels[item["business_code"]] = requests.get(f"https://tim-loonie-94123.herokuapp.com/business/{item['id']}/labels")

        for label in labels[item["business_code"]].json():
            beetrack_dispatch_response = label.get("beetrack_dispatch_response")
            if beetrack_dispatch_response and "identifier" in beetrack_dispatch_response.get("response", {}):
                if beetrack_dispatch_response["response"]["identifier"].lower() == data["identifier"].lower() or ('groups' in data and data['groups'] and 'name' in data['groups'][0] and data['groups'][0]['name'].upper() == item["name"].upper()):
                    business_code = item["business_code"]
                    break

    if business_code == "doto":
        requests.post("https://sandboxshipmentsapi.doto.com.mx/api/v1/webhooks/enviadero/tracker", json=data)
        requests.post("https://shipmentsapi.doto.com.mx/api/v1/webhooks/enviadero/tracker", json=data)
        print("Data success sent for Doto")
        return "Data success sent for Doto"
    elif business_code == "xiaomi":
        print("Data success sent for Xiaomi")
        return "Data success sent for Xiaomi"
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
    app.run(host='0.0.0.0', port='3000', debug=True)