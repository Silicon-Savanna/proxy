from rest_framework.views import APIView
from rest_framework.response import Response

class ProxyView(APIView):       
    def post(self, request):
        # get payload from request at json

        print(request)
        print(request.data)
        return Response({'hello': 'world'})