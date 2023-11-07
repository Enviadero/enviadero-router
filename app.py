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

    business = requests.get("https://tim-loonie-94123.herokuapp.com/business")

    labels = {}
    business_code = None

    for item in business.json():
        labels[item["business_code"]] = requests.get(f"https://tim-loonie-94123.herokuapp.com/business/{item['id']}/labels")

        for label in labels[item["business_code"]].json():
            beetrack_dispatch_response = label.get("beetrack_dispatch_response")
            if beetrack_dispatch_response and "identifier" in beetrack_dispatch_response.get("response", {}):
                if beetrack_dispatch_response["response"]["identifier"] == data["identifier"]:
                    business_code = item["business_code"]
                    break

    if business_code == "enviadero":
        return "Data success sent for Doto"
    elif business_code == "xiaomi":
        return "Data success sent for Xiaomi"
    else:
        return "Business not found"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)