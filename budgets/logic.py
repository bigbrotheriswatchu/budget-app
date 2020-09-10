from datetime import date
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView
from .models import BudgetData, Budget, DailySpend, MonthlySpend, YearlySpend


def _update_or_create_daily_costs(values, queryset):
    obj, created = DailySpend.objects.update_or_create(today_spend_date=timezone.now(),
                                                       defaults=values)
    if obj:
        queryset = queryset.values_list('pk', flat=True)
        obj.today_budget_info.add(*queryset)


class BudgetDataDailyCost(ListView):
    """
    Getting Daily Costs.

    Filter of queryset by today budget data,
    get costs values and update or create :model:DailyCost

    """
    model = BudgetData

    def get_queryset(self):
        self.budget = get_object_or_404(Budget, pk=self.kwargs['pk'])

        today = timezone.now()

        today_budget_info = self.budget.budgetdata_set.filter(pub_date__date=today)
        month_budget_info = self.budget.budgetdata_set.filter(pub_date__month=today.month)
        year_budget_info = self.budget.budgetdata_set.filter(pub_date__year=today.year)

        spent_today_budget_info = today_budget_info.values_list('amount_spent', flat=True)
        spent_month_budget_info = month_budget_info.values_list('amount_spent', flat=True)
        spent_year_budget_info = year_budget_info.values_list('amount_spent', flat=True)

        today_values = {'budget': self.budget,
                        'today_spend_date': today,
                        'amount_expense': sum(spent_today_budget_info)}

        month_values = {'budget': self.budget,
                        'month_spend_date': today.month,
                        'amount_expense': sum(spent_month_budget_info)}

        year_values = {'budget': self.budget,
                       'year_spend_date': today.year,
                       'amount_expense': sum(spent_year_budget_info)}

        _update_or_create_daily_costs(today_values, today_budget_info)
