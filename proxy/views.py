from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json

class ProxyView(APIView):       
    def post(self, request):
        
        # convert request.data to json
        entry = json.loads(request.body)
        message_type = entry['entry'][0]['changes'][0]['value']['messages'][0]['type']
        print(entry)
        if message_type == 'text':
            name = entry['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
            phone_number = entry['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
            
            message_body = entry['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            print(f'phone_number: {phone_number}')
            print(f'phone_number: {name}')
            print(f'message_body: {message_body}')
            print(f'message_type: {message_type}')
        
        if message_type == 'image':
            
            image = entry['entry'][0]['changes'][0]['value']['messages'][0]['image']
            get_media_url(image['id'])
            print(image)
        
        
        
        return Response({'hello': 'world'})
    
def get_media_url(media_id):    
    url = f"https://graph.facebook.com/v17.0/{media_id}"

    payload = {}
    headers = {
    'Authorization': 'Bearer EAAIZAebVGy5sBAGckoG1xOp7DZAgQ5uu227G5gtN8YFEhQA5gZCxGcLK1cvPVPgm2Aa6WYQZBCLMkNFvBZBATEeebih6cAfuhOXb8KzGpWW9tGoaYZAFH4m3VLe5XXuKHNXFZBlWJlvvn4JBKQTzyTb0hGUq3clZAUU22miJs0V4rVhlGZCsxyyZB0'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response)
    # print(json.loads(response))