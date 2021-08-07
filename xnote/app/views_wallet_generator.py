from django.shortcuts import render

from .models import WalletAccount, WalletCredit, WalletDeposit, WalletIncome, WalletExpense, WalletCar, WalletHouse


def wallet_generator_year_month(request, year, month):
    year_prev = int(year) - 1 if int(month) == 1 else year
    month_prev = int(month) - 1 if int(month) > 1 else 12

    filterArgsByYearMonth = {'year': year_prev, 'month': month_prev}
    wallet_accounts = WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('-type', 'name')
    wallet_deposits = WalletDeposit.objects.filter(**filterArgsByYearMonth).order_by('name')
    wallet_credits = WalletCredit.objects.filter(**filterArgsByYearMonth).order_by('name')
    filterArgsByYearMonthRegular = {'year': year_prev, 'month': month_prev, 'type': 'regular'}
    wallet_incomes = WalletIncome.objects.filter(**filterArgsByYearMonthRegular).order_by('type', 'name')
    wallet_expenses = WalletExpense.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
    wallet_houses = WalletHouse.objects.filter(**filterArgsByYearMonth).order_by('name')
    wallet_cars = WalletCar.objects.filter(**filterArgsByYearMonth).order_by('exploitation')

    log = []
    for wallet_account in wallet_accounts:
        log.append("New account \"" + str(wallet_account.name) + " " + str(wallet_account.value) + " " + str(wallet_account.currency) + " " + str(wallet_account.type) + "\"")
        WalletAccount.objects.create(name=wallet_account.name,
                                     value=wallet_account.value,
                                     currency=wallet_account.currency,
                                     type=wallet_account.type,
                                     year=year,
                                     month=month)

    log.append("")
    for wallet_deposit in wallet_deposits:
        log.append("New deposit \"" + str(wallet_deposit.name) + " " + str(wallet_deposit.value) + " " + str(wallet_deposit.rate) + "\"")
        WalletDeposit.objects.create(name=wallet_deposit.name,
                                    value=wallet_deposit.value,
                                    rate=wallet_deposit.rate,
                                    year=year,
                                    month=month)

    log.append("")
    for wallet_credit in wallet_credits:
        log.append("New credit \"" + str(wallet_credit.name) + " " + str(wallet_credit.value) + " " + str(wallet_credit.rate) + " " + str(wallet_credit.balance) + "\"")
        WalletCredit.objects.create(name=wallet_credit.name,
                                    value=wallet_credit.value,
                                    rate=wallet_credit.rate,
                                    balance=wallet_credit.balance,
                                    interest=0.0,
                                    insurance=0.0,
                                    capital=0.0,
                                    year=year,
                                    month=month)

    log.append("")
    for wallet_income in wallet_incomes:
        log.append("New income \"" + str(wallet_income.name) + " " + str(wallet_income.type) + "\"")
        WalletIncome.objects.create(name=wallet_income.name,
                                     value=0.0,
                                     type=wallet_income.type,
                                     year=year,
                                     month=month)

    log.append("")
    for wallet_expense in wallet_expenses:
        log.append("New expense \"" + str(wallet_expense.name) + "\"")
        WalletExpense.objects.create(name=wallet_expense.name,
                                   value=0.0,
                                   type=wallet_expense.type,
                                   year=year,
                                   month=month)

    log.append("")
    for wallet_house in wallet_houses:
        log.append("New house \"" + str(wallet_house.name) + "\"")
        WalletHouse.objects.create(name=wallet_house.name,
                                 value=0.0,
                                 year=year,
                                 month=month)

    wallet_car = wallet_cars.last()
    if wallet_car:
        log.append("")
        log.append("New car \"" + str(wallet_car.car) + " " + str(wallet_car.exploitation) + "\"")
        WalletCar.objects.create(car=wallet_car.car,
                                 exploitation=wallet_car.exploitation,
                                 refuelling=0.0,
                                 payment=0.0,
                                 year=year,
                                 month=month)

    return render(request, 'app/wallet_generator.html', {
        'year': year,
        'month': month,
        'log': log
    })


def wallet_clear_year_month(request, year, month):
    filterArgsByYearMonth = {'year': year, 'month': month}
    wallet_accounts = WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('-type', 'name')
    wallet_deposits = WalletDeposit.objects.filter(**filterArgsByYearMonth).order_by('name')
    wallet_credits = WalletCredit.objects.filter(**filterArgsByYearMonth).order_by('name')
    wallet_incomes = WalletIncome.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
    wallet_expenses = WalletExpense.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
    wallet_houses = WalletHouse.objects.filter(**filterArgsByYearMonth).order_by('name')
    wallet_cars = WalletCar.objects.filter(**filterArgsByYearMonth).order_by('exploitation')

    log = []
    for wallet_account in wallet_accounts:
        log.append("Clear account \"" + str(wallet_account.name) + " " + str(wallet_account.value) + " " + str(wallet_account.type) + "\"")
        WalletAccount.objects.get(id=wallet_account.id).delete()

    log.append("")
    for wallet_deposit in wallet_deposits:
        log.append("Clear deposit \"" + str(wallet_deposit.name) + " " + str(wallet_deposit.value) + " " + str(wallet_deposit.rate) + "\"")
        WalletDeposit.objects.get(id=wallet_deposit.id).delete()

    log.append("")
    for wallet_credit in wallet_credits:
        log.append("Clear credit \"" + str(wallet_credit.name) + " " + str(wallet_credit.value) + " " + str(wallet_credit.rate) + " " + str(wallet_credit.balance) + "\"")
        WalletCredit.objects.get(id=wallet_credit.id).delete()

    log.append("")
    for wallet_income in wallet_incomes:
        log.append("Clear income \"" + str(wallet_income.name) + " " + str(wallet_income.type) + "\"")
        WalletIncome.objects.get(id=wallet_income.id).delete()

    log.append("")
    for wallet_expense in wallet_expenses:
        log.append("Clear expense \"" + str(wallet_expense.name) + "\"")
        WalletExpense.objects.get(id=wallet_expense.id).delete()

    log.append("")
    for wallet_house in wallet_houses:
        log.append("Clear house \"" + str(wallet_house.name) + "\"")
        WalletHouse.objects.get(id=wallet_house.id).delete()

    log.append("")
    for wallet_car in wallet_cars:
        log.append("Clear car \"" + str(wallet_car.car) + " " + str(wallet_car.exploitation) + "\"")
        WalletCar.objects.get(id=wallet_car.id).delete()

    return render(request, 'app/wallet_generator.html', {
        'year': year,
        'month': month,
        'log': log
    })