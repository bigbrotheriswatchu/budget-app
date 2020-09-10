from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse
from django.utils import timezone


class Budget(models.Model):
    """
    Model for containerising budget information.

    example: budget 2020, budget 2021.

    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, verbose_name="Название бюджета")
    budget_description = models.TextField(max_length=300, blank=True, verbose_name="Описание")
    common_cost = models.FloatField(default=0, verbose_name="Общая сумма затрат")
    balance = models.FloatField(default=0, verbose_name="Осталось средств")
    my_funds = models.FloatField(default=0, verbose_name="Мои средства")
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.balance = self.my_funds
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('budget_list', kwargs={'pk': self.pk})


class BudgetData(models.Model):
    """
    Model for budget information,
    like name of expanse, costs, date.

    """
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, verbose_name='Список бюджетов')
    expense_name = models.CharField(max_length=255, verbose_name='На что потраченно')
    amount_spent = models.FloatField(default=0, verbose_name='Потраченная сумма')
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.expense_name

    def get_absolute_url(self):
        return reverse('budget_data_list', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.pk:
            Budget.objects.filter(pk=self.budget.pk).update(
                common_cost=F('common_cost') + self.amount_spent,
                balance=F('my_funds') - self.amount_spent,
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Overridden delete method.

        Field common_costs from related :model:`budget.Budget`,
        gets update after deleting

        """
        Budget.objects.filter(pk=self.budget.pk).update(
            common_cost=F('common_cost') - self.amount_spent,
            balance=F('balance') + self.amount_spent,
        )
        super().delete(*args, **kwargs)


class DailySpend(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, verbose_name="Бюджет")

    today_budget_info = models.ManyToManyField(
        BudgetData,
        verbose_name="Данные за сегодня",
        related_name="today_budget_info"
    )
    amount_expense = models.FloatField(default=0, verbose_name='Ежедневная сумма затрат')
    today_spend_date = models.DateField(default=timezone.now(), verbose_name='День затрат')

    def __str__(self):
        return 'затраты за ' + str(self.today_spend_date)


class MonthlySpend(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, verbose_name="Бюджет")

    monthly_budget_info = models.ManyToManyField(
        BudgetData,
        verbose_name="Данные за месяц",
        related_name="monthly_budget_info"
    )
    amount_expense = models.FloatField(default=0, verbose_name='Месячная сумма затрат')
    month_spend_date = models.DateField(default=timezone.now().month, verbose_name='Месяц затрат')

    def __str__(self):
        return 'затраты за ' + str(self.month_spend_date)


class YearlySpend(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, verbose_name="Бюджет")
    yearly_budget_info = models.ManyToManyField(
        BudgetData,
        verbose_name="Данные за год",
        related_name="yearly_budget_info"
    )
    amount_expense = models.FloatField(default=0, verbose_name='Годовая сумма затрат')
    year_spend_date = models.DateField(default=timezone.now().year, verbose_name='Год затртат')

    def __str__(self):
        return 'затраты за ' + str(self.year_spend_date)
