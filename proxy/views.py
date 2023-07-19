from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json

class ProxyView(APIView):       
    def post(self, request):
        
        # convert request.data to json
        entry = json.loads(request.body)
        message_type = entry['entry'][0]['changes'][0]['value']['messages'][0]['type']
        # print(entry)
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
            print(image['id'])
        
        
        
        return Response({'hello': 'world'})
    
def get_media_url(media_id):    
    import requests

    url = "https://graph.facebook.com/v17.0/6517166938366080"

    payload = {}
    headers = {
    'Authorization': 'Bearer EAAIZAebVGy5sBAMQ8L6OxYACJKZCTxQWnFjms3vd8ZBiVJ4KVVrh47X3t7DY974Xx4GZBOc3P7H0O5e4nNDKC3ZAnIbg0Wk35NhoSHJqMKj6e4FvZC6WinE9qJ9SJaQOfBuiHTZC8vhjsbKtUSm0YRsI2Ia9aZCwf8j1LWChf2L7EmYmAOtKwdmr'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)