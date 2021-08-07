from django.shortcuts import render

from .models import WalletAccount, WalletDeposit, WalletCredit, WalletIncome, WalletExpense, WalletHouse, WalletCar, \
    Reminder


def search(request):
    search_value = ""
    limit = 64
    if request.method == "POST":
        search_value = request.POST.get("search_value", "")
    reminders = Reminder.objects.filter(name__icontains=search_value).order_by('-modified')[:limit]
    wallet_accounts = WalletAccount.objects.filter(name__icontains=search_value).order_by('-modified')[:limit]
    wallet_deposits = WalletDeposit.objects.filter(name__icontains=search_value).order_by('-modified')[:limit]
    wallet_credits = WalletCredit.objects.filter(name__icontains=search_value).order_by('-modified')[:limit]
    wallet_incomes = WalletIncome.objects.filter(name__icontains=search_value).order_by('-modified')[:limit]
    wallet_expenses = WalletExpense.objects.filter(name__icontains=search_value).order_by('-modified')[:limit]
    wallet_houses = WalletHouse.objects.filter(name__icontains=search_value).order_by('-modified')[:limit]
    wallet_cars = WalletCar.objects.filter(car__icontains=search_value).order_by('-modified')[:limit]
    return render(request, 'app/search.html',
                    {
                        'search_value': search_value,
                        'reminders': reminders,
                        'wallet_accounts': wallet_accounts,
                        'wallet_deposits': wallet_deposits,
                        'wallet_credits': wallet_credits,
                        'wallet_incomes': wallet_incomes,
                        'wallet_expenses': wallet_expenses,
                        'wallet_houses': wallet_houses,
                        'wallet_cars': wallet_cars,
                    })
