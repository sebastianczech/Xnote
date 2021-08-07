from django.shortcuts import render

from .service_wallet_car import calculate_car_fuel_consumption


def wallet_car_year_month(request):

    wallet_cars_sum_grouped_by_name_year_month = calculate_car_fuel_consumption()

    return render(request, 'app/wallet_car.html', {
        'wallet_cars_sum_grouped_by_name_year_month': wallet_cars_sum_grouped_by_name_year_month
    })