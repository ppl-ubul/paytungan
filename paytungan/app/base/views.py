from django.http import JsonResponse
from django.db import connection
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny


@permission_classes([AllowAny])
class HealthCheckViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return JsonResponse({"message": "OK"}, status=200)
        except Exception as ex:
            return JsonResponse({"error": str(ex)}, status=500)
