from django import forms
from .models import BudgetData, Budget


class BudgetDataForm(forms.ModelForm):
    class Meta:
        model = BudgetData
        fields = ['budget', 'expense_name', 'amount_spent']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'my_funds', 'budget_description']

        widgets = {
            'budget_description': forms.Textarea(
                attrs={'rows': 2, 'cols': 20,
                       'placeholder': 'Введите описание'}
            ),

            'name': forms.TextInput(
                attrs={'placeholder': 'Введите описание'}
            )
        }


