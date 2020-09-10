from .models import BudgetData
from rest_framework import serializers


class BudgetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetData
        fields = '__all__'
