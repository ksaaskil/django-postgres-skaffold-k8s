from django.db import connection
from django.http import HttpResponse

def index(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return HttpResponse(status=200)
    except Exception as ex:
        return HttpResponse(status=500)
