from decimal import Decimal

from django.db.models import Sum, Min, Max

from .models import WalletCar


def calculate_car_fuel_consumption():
    wallet_cars_sum_grouped_by_name_year_month = WalletCar.objects \
        .values('year', 'month', 'currency') \
        .annotate(total_value=Sum('payment'),
                  total_refuelling=Sum('refuelling'),
                  total_distance=Max('exploitation') - Min('exploitation'),
                  exploitation_min=Min('exploitation'),
                  exploitation_max=Max('exploitation')) \
        .order_by('currency', 'year', 'month', )

    for wallet_car in wallet_cars_sum_grouped_by_name_year_month:
        if wallet_car['total_distance'] > 0:
            wallet_car['avg_refuelling_100km'] = round(
                100 * wallet_car['total_refuelling'] / wallet_car['total_distance'], 2)
            wallet_car['avg_price'] = round(wallet_car['total_value'] / wallet_car['total_refuelling'], 2)
        else:
            wallet_car['avg_refuelling_100km'] = Decimal(0.0)
            wallet_car['avg_price'] = Decimal(0.0)
    return wallet_cars_sum_grouped_by_name_year_month