from rest_framework.views import APIView
from rest_framework.response import Response
import pprint
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
            print(image)
        
        
        
        return Response({'hello': 'world'})