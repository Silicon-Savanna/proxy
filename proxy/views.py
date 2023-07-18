from rest_framework.views import APIView
from rest_framework.response import Response
import pprint

class ProxyView(APIView):       
    def post(self, request):
        pprint(request.data)
        # convert request.data to json
        json_data = request.data.get('json')
        pprint(json_data)
        
        return Response({'hello': 'world'})