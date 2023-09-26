import json
import requests
import os
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from . import settings
import logging

logger = logging.getLogger(__name__)

class ProxyView(APIView):
    """
    View to handle the proxy requests and redirect traffic from WhatsApp Cloud API to Custom Server
    """

    def post(self, request):
        print(request.body.decode())
        entry = json.loads(request.body.decode())

        # Get message type
        try:
            message_type = entry["entry"][0]["changes"][0]["value"]["messages"][0]["type"]
        except KeyError:
            return Response({"error": "Service not active"}, status=405)

        # Extract relevant information from the message
        name = entry["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
        phone_number = entry["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]

        # Extract the message body based on the message type
        if message_type == "text":
            message_body = entry["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        else:
            if message_type == "image":
                message_body = entry["entry"][0]["changes"][0]["value"]["messages"][0]["image"]["id"]
                media_url = get_media_url(message_body)
            elif message_type == "document":
                message_body = entry["entry"][0]["changes"][0]["value"]["messages"][0]["document"]["id"]
                media_url = get_media_url(message_body)
            elif message_type == "video":
                message_body = entry["entry"][0]["changes"][0]["value"]["messages"][0]["video"]["id"]
                media_url = get_media_url(message_body)
            elif message_type == "audio":
                message_body = entry["entry"][0]["changes"][0]["value"]["messages"][0]["audio"]["id"]
                media_url = get_media_url(message_body)
            else:
                return Response({"error": "Invalid message type"}, status=400)

            # If image URL is available, replace the message_body with it
            if media_url is not None:
                message_body = media_url

        # Custom server URL where you want to redirect the traffic
        url = settings.REDIRECT_URL
        logger.info(f"Phone number: {phone_number}, Message type: {message_type}, Message body: {message_body}")
        # Set the payload as it is on your custom server
        payload = json.dumps({
            "phone_number": phone_number,
            "message_type": message_type,
            "message": message_body,
            "name": name,
        })

        headers = {
            "Content-Type": "application/json",
            "Cookie": "csrftoken=5tq6VqUIRj96bOOvCvTaWlAv1WVBvLSc",
        }

        # Make the request to the custom server
        with requests.post(url, headers=headers, data=payload) as response:
            # Check the response status and return appropriate response
            if response.status_code == 200:
                return Response({"status": "Success"}, status=200)
            else:
                return Response({"status": "Failed"}, status=400)

class FacebookWebhookView(APIView):
    def post(self, request):
        logger.info("-------------- New Request POST --------------")
        logger.info("Headers: %s", request.headers)
        logger.info("Body: %s", request.data)
        return Response({"message": "Thank you for the message"})

    def get(self, request):
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        logger.info("-------------- New Request GET --------------")
        logger.info("Headers: %s", request.headers)
        logger.info("Body: %s", request.data)

        if mode and token:
            if mode == "subscribe" and token == "12345":
                logger.info("WEBHOOK_VERIFIED")
                return Response(challenge, status=200)
            else:
                logger.info("Responding with 403 Forbidden")
                return Response(status=403)

        logger.info("Replying Thank you.")
        return Response({"message": "Thank you for the message"})

def get_media_url(media_id: str) -> str:
    # Fetch the image URL using the Facebook Graph API
    url = f"https://graph.facebook.com/v17.0/{media_id}"
    ACCESS_TOKEN = os.environ["API_KEY"]
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    with requests.get(url, headers=headers) as response:
        # If the request was successful, get the image content and store it in S3 or handle it in your own way
        if response.status_code == 200:
            json_data = response.json()
            downloaded_image = requests.get(json_data["url"], headers=headers)

            if settings.STORE_TO_S3 == "True":
                url = upload_to_s3(downloaded_image.content, media_id)
            else:
                """
                Handle image storage in your own way
                """
                url = json_data["url"]  # Replace this with your custom URL
            return url

    return ""

def upload_to_s3(file_hash: bytes, media_id: str) -> str:
    # Uploads the file to S3
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
