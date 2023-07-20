from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
import boto3


class ProxyView(APIView):
    """
    View to handle the proxy requests and redirect traffic from WhatsApp Cloud API to Custom Server
    """
    def post(self, request):     
        entry = json.loads(request.body)
        try:
            message_type = entry["entry"][0]["changes"][0]["value"]["messages"][0][
                "type"
            ]
        except KeyError:
            # return method not allowed
            return Response({"error": "Service not active"}, status=405)

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
            image_url = get_media_url(message_body)
            if image_url is None:
                pass
            else:
                message_body = image_url

        print(f"phone_number: {phone_number}")
        print(f"phone_number: {name}")
        print(f"message_body: {message_body}")
        print(f"message_type: {message_type}")
        url = "http://remit-loadb-ix52djo49no0-d833d409760e1a68.elb.us-east-1.amazonaws.com:5000/api/v1/index/"

        payload = json.dumps(
            {
                "phone_number": phone_number,
                "message_type": message_type,
                "message": message_body,
                "name": name,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Cookie": "csrftoken=5tq6VqUIRj96bOOvCvTaWlAv1WVBvLSc",
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

        return Response({"status": "Success"}, status=200)


def get_media_url(media_id):
    import requests

    url = f"https://graph.facebook.com/v17.0/{media_id}"

    payload = {}
    import os

    ACCESS_TOKEN = os.environ["API_KEY"]
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers, params=payload)
    print(response.content)
    # response to json
    if response.status_code == 200:
        json_data = response.json()
        payload = {}
        print(headers)
        downloaded_image = requests.get(json_data["url"], headers=headers)
        upload_to_s3(downloaded_image.content, media_id)
        return url
    return None


def upload_to_s3(file_hash, media_id):
    """
    Uploads the file to S3
    """
    s3 = boto3.resource('s3',
        aws_access_key_id='AKIAWK7RWTONRM2BTUWP',
        aws_secret_access_key= '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',
        )
    bucket = s3.Bucket('remitimages')
    media_id = media_id + ".jpg"
    bucket.put_object(Key=media_id, Body=file_hash)
    url = f"https://remitimages.s3.amazonaws.com/{media_id}"
    return url
