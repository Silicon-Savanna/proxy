from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json


class ProxyView(APIView):
    def post(self, request):
        # convert request.data to json
        entry = json.loads(request.body)
        message_type = entry["entry"][0]["changes"][0]["value"]["messages"][0]["type"]
        name = entry["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"][
            "name"
        ]
        phone_number = entry["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
        # print(entry)
        if message_type == "text":
            message_body = entry["entry"][0]["changes"][0]["value"]["messages"][0][
                "text"
            ]["body"]
        elif message_type == "image":
            message_body = entry["entry"][0]["changes"][0]["value"]["messages"][0][
                "image"
            ]["id"]

        print(f"phone_number: {phone_number}")
        print(f"phone_number: {name}")
        print(f"message_body: {message_body}")
        print(f"message_type: {message_type}")
        url = "http://remit-loadb-ix52djo49no0-d833d409760e1a68.elb.us-east-1.amazonaws.com:5000/api/v1/index/"

        payload = json.dumps({
        "phone_number": phone_number,
        "message_type": message_type,
        "message": message_body,
        "name": name
        })
        headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=5tq6VqUIRj96bOOvCvTaWlAv1WVBvLSc'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

        return Response({"hello": "world"})


def get_media_url(media_id):
    import requests

    url = "https://graph.facebook.com/v17.0/6517166938366080"

    payload = {}
    headers = {
        "Authorization": "Bearer EAAIZAebVGy5sBAMQ8L6OxYACJKZCTxQWnFjms3vd8ZBiVJ4KVVrh47X3t7DY974Xx4GZBOc3P7H0O5e4nNDKC3ZAnIbg0Wk35NhoSHJqMKj6e4FvZC6WinE9qJ9SJaQOfBuiHTZC8vhjsbKtUSm0YRsI2Ia9aZCwf8j1LWChf2L7EmYmAOtKwdmr"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
