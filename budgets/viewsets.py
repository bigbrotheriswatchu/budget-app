from rest_framework import viewsets
from .serializers import BudgetDataSerializer
from .models import BudgetData


class BudgetDataViewSet(viewsets.ModelViewSet):
    queryset = BudgetData.objects.all()
    serializer_class = BudgetDataSerializer
