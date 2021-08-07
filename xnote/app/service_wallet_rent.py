from decimal import Decimal

from django.db.models import Sum

from .models import WalletIncome, WalletExpense


def calculate_rent_tax():
    wallet_rents_sum_grouped_by_name_year_month = WalletIncome.objects \
        .filter(name__contains="Wynajem") \
        .filter(year__gte=2019) \
        .values('year', 'month', 'currency') \
        .annotate(total_value=Sum('value')) \
        .order_by('currency', 'year', 'month', )
    # .filter(value__gt=0) \

    global_total_tax = Decimal(0.0)
    global_paid_tax = Decimal(0.0)
    global_currency = ""
    for wallet_rent in wallet_rents_sum_grouped_by_name_year_month:
        wallet_rent['total_tax'] = round(8.5 * float(wallet_rent['total_value']) / 100, 2)
        global_currency = wallet_rent['currency']
        global_total_tax = Decimal(round(global_total_tax + Decimal(round(wallet_rent['total_tax'], 2)), 2))
        try:
            wallet_paid_tax_for_year_month = WalletExpense.objects.get(name='Podatek ryczałtowy za wynajem',
                                                                       year=wallet_rent['year'],
                                                                       month=wallet_rent['month'])
            global_paid_tax = global_paid_tax + wallet_paid_tax_for_year_month.value
        except WalletExpense.DoesNotExist:
            wallet_paid_tax_for_year_month = None

        if wallet_paid_tax_for_year_month:
            wallet_rent['paid_tax'] = wallet_paid_tax_for_year_month.value
        else:
            wallet_rent['paid_tax'] = Decimal(0.0)

    return wallet_rents_sum_grouped_by_name_year_month, global_total_tax, global_paid_tax, global_currency