from django.conf.urls import url
from django.urls import path

from .views import BudgetView, BudgetInfoView, UpdateBudgetDataView, DeleteBudgetDataView, TestFilter
urlpatterns = [
    path('home/', BudgetView.as_view(), name="budget_list"),
    url(r'budget_info/(?P<pk>[\d]+)/$', BudgetInfoView.as_view(), name="budget_data_list"),
    url(r'update_budget_data/(?P<pk>[\d]+)/$', UpdateBudgetDataView.as_view(), name='update_budget_data'),
    url(r'delete_budget_data/(?P<pk>[\d]+)/$', DeleteBudgetDataView.as_view(), name='delete_budget_data'),
    url(r'budget_filter/(?P<pk>[\d]+)/$', TestFilter.as_view(), name="filter"),

]
