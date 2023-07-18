from rest_framework.views import APIView
from rest_framework.response import Response
import pprint
import json

class ProxyView(APIView):       
    def post(self, request):
        
        # convert request.data to json
        entry = json.loads(request.data)
        phone_number = entry['changes'][0]['value']['metadata']['display_phone_number']
        message_body = entry['changes'][0]['value']['messages'][0]['text']['body']
        message_type = entry['changes'][0]['value']['messages'][0]['type']
        print(f'phone_number: {phone_number}')
        print(f'message_body: {message_body}')
        print(f'message_type: {message_type}')
        print(f'entry: {entry}')
        
        return Response({'hello': 'world'})