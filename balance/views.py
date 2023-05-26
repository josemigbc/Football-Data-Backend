from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BalanceSerializer
from .models import Balance

# Create your views here.

class BalanceView(APIView):
    def get(self,request):
        serializer = BalanceSerializer(Balance.objects.get(user=request.user))
        return Response(serializer.data)