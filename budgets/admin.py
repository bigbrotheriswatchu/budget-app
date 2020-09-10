from django.contrib import admin
from .models import Budget, BudgetData, DailySpend, MonthlySpend, YearlySpend


class BudgetAdmin(admin.ModelAdmin):
    pass


class BudgetInfoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Budget, BudgetAdmin)
admin.site.register(BudgetData, BudgetInfoAdmin)
admin.site.register(DailySpend)
admin.site.register(MonthlySpend)
admin.site.register(YearlySpend)

