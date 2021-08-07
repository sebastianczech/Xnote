from django.db.models import Sum
from django.shortcuts import render

from .models import WalletAccount, WalletCredit, WalletDeposit, WalletIncome, WalletExpense, WalletCar


def wallet_analytics_year_month(request):
    wallet_accounts_sum_grouped_by_name_year_month = WalletAccount.objects\
        .values('year', 'month', 'currency')\
        .annotate(total_value=Sum('value'))\
        .order_by('currency', 'year', 'month',)

    wallet_deposits_sum_grouped_by_name_year_month = WalletDeposit.objects \
        .values('year', 'month', 'currency') \
        .annotate(total_value=Sum('value')) \
        .order_by('currency', 'year', 'month', )

    wallet_credits_sum_grouped_by_name_year_month = WalletCredit.objects \
        .values('year', 'month', 'currency') \
        .annotate(total_value=Sum('balance')) \
        .order_by('currency', 'year', 'month', )

    wallet_incomes_sum_grouped_by_name_year_month = WalletIncome.objects \
        .values('year', 'month', 'currency') \
        .annotate(total_value=Sum('value')) \
        .order_by('currency', 'year', 'month', )

    wallet_expenses_sum_grouped_by_name_year_month = WalletExpense.objects \
        .values('year', 'month', 'currency') \
        .annotate(total_value=Sum('value')) \
        .order_by('currency', 'year', 'month', )

    wallet_cars_sum_grouped_by_name_year_month = WalletCar.objects \
        .values('year', 'month', 'currency') \
        .annotate(total_value=Sum('payment')) \
        .order_by('currency', 'year', 'month', )

    return render(request, 'app/wallet_analytics.html', {
        'wallet_accounts_sum_grouped_by_name_year_month': wallet_accounts_sum_grouped_by_name_year_month,
        'wallet_deposits_sum_grouped_by_name_year_month': wallet_deposits_sum_grouped_by_name_year_month,
        'wallet_credits_sum_grouped_by_name_year_month': wallet_credits_sum_grouped_by_name_year_month,
        'wallet_incomes_sum_grouped_by_name_year_month': wallet_incomes_sum_grouped_by_name_year_month,
        'wallet_expenses_sum_grouped_by_name_year_month': wallet_expenses_sum_grouped_by_name_year_month,
        'wallet_cars_sum_grouped_by_name_year_month': wallet_cars_sum_grouped_by_name_year_month
    })