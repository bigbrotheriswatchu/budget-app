from datetime import date

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from .models import Budget, DailySpend, BudgetData
from .logic import BudgetDataDailyCost
from .forms import BudgetDataForm, BudgetForm


class BudgetView(CreateView, ListView):
    """View for home page.

    Shows list of your budgets like: budget 2020, budget 2021

    Shows creation form for Budget

    """
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/index.html'
    success_url = '/home'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BudgetInfoView(CreateView, BudgetDataDailyCost):
    """Logic for BudgetData.

    Gets creation form for :model:BudgetData.

    Returns context for Budget, BudgetData and DailyCost.

    Makes daily costs from BudgetDataDailyCost class.

    """
    model = BudgetData
    form_class = BudgetDataForm
    template_name = 'budgets/budget_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['budget'] = self.budget
        context['daily_costs'] = get_object_or_404(DailySpend, today_spend_date=date.today())
        context['budget_data'] = self.budget.budgetdata_set.all()

        return context

    def get_success_url(self):
        return reverse("budget_data_list", kwargs={'pk': self.object.budget.pk})


class UpdateBudgetDataView(UpdateView):
    """
    Getting budget information by pk for edit
    and redirect on the budget_info.html

    """
    model = BudgetData
    template_name = 'budgets/update_budget_data.html'
    form_class = BudgetDataForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("budget_data_list", kwargs={'pk': self.object.budget.pk})


class DeleteBudgetDataView(DeleteView):
    """Delete budgets data."""

    model = BudgetData
    template_name = 'budgets/budget_info.html'

    def get_success_url(self):
        return reverse("budget_data_list", kwargs={'pk': self.object.budget.pk})


def filter_data(queryset, parm1):
    return queryset.filter(parm1)


class TestFilter(ListView):
    model = BudgetData
    template_name = 'budgets/test.html'

    def get_queryset(self):
        self.budget = get_object_or_404(Budget, pk=self.kwargs['pk'])
        today = date.today()
        _filter = self.budget.budgetdata_set.filter(date__year=today.year)
        return _filter
