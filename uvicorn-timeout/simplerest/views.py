from rest_framework.viewsets import ViewSet 
from rest_framework.views import APIView
from rest_framework.response import Response
import time
from simplerest.models import Book

class MainViewset(ViewSet):
    def list(self, request):
        time.sleep(20)
        return Response({"message":"good"})


class BookView(APIView):
    def post(self, request, **kwargs):
        new_book = request.data["book"]
        Book(*new_book).save()
        return Response("it worked, I think")
