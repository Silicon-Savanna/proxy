from rest_framework.views import APIView
from rest_framework.response import Response
import pprint
import json

class ProxyView(APIView):       
    def post(self, request):
        
        # convert request.data to json
        entry = json.loads(request.body)
        phone_number = entry['entry'][0]['changes'][0]['value']['progile']['wa_id']
        name = entry['entry'][0]['changes'][0]['value']['profile']['name']
        message_body = entry['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        message_type = entry['entry'][0]['changes'][0]['value']['messages'][0]['type']

        print(f'phone_number: {phone_number}')
        print(f'phone_number: {name}')
        print(f'message_body: {message_body}')
        print(f'message_type: {message_type}')
        
        
        return Response({'hello': 'world'})