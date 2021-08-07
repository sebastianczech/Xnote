from django.shortcuts import render

from .service_wallet_rent import calculate_rent_tax


def wallet_rent_year_month(request):
    wallet_rents_sum_grouped_by_name_year_month, global_total_tax, global_paid_tax, global_currency = calculate_rent_tax()

    return render(request, 'app/wallet_rent.html', {
        'wallet_rents_sum_grouped_by_name_year_month': wallet_rents_sum_grouped_by_name_year_month,
        'global_total_tax': global_total_tax,
        'global_paid_tax': global_paid_tax,
        'global_currency': global_currency
    })