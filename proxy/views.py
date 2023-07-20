from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import os
import json
import boto3
import settings


class ProxyView(APIView):
    """
    View to handle the proxy requests and redirect traffic from WhatsApp Cloud API to Custom Server
    """

    def post(self, request):
        entry = json.loads(request.body)
        # Get message type
        try:
            message_type = entry["entry"][0]["changes"][0]["value"]["messages"][0][
                "type"
            ]
        except KeyError:
            return Response({"error": "Service not active"}, status=405)

        name = entry["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"][
            "name"
        ]
        phone_number = entry["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
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
        url = settings.REDIRECT_URL
        # Set the payload as it is on your custom server
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
        if response.status_code == 200:
            return Response({"status": "Success"}, status=200)
        else:
            return Response({"status": "Failed"}, status=400)

def get_media_url(media_id):
    url = f"https://graph.facebook.com/v17.0/{media_id}"    
    ACCESS_TOKEN = os.environ["API_KEY"]
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        downloaded_image = requests.get(json_data["url"], headers=headers)
        if settings.STORE_TO_S3 == "True":
            url = upload_to_s3(downloaded_image.content, media_id)
        else:
            """
            Handle image storage in your own way
            """
            url = "hrr"
        return url
    return None


def upload_to_s3(file_hash, media_id):
    """
    Uploads the file to S3
    """
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
    media_id = media_id + ".jpg"
    bucket.put_object(Key=media_id, Body=file_hash)
    url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{media_id}"
    return url
