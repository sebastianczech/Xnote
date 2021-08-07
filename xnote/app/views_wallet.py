from datetime import datetime
from decimal import Decimal

from bson import json_util
from django.core.serializers import serialize
from django.db.models import Sum, Max, Min
from django.shortcuts import render, redirect, get_object_or_404

from . import mongoDatabase
from .forms import WalletAccountForm, WalletCreditForm, WalletDepositForm, WalletIncomeForm, WalletExpenseForm, \
    WalletCarForm, WalletHouseForm
from .models import WalletAccount, WalletCredit, WalletDeposit, WalletIncome, WalletExpense, WalletCar, WalletHouse


def wallet(request):
    return wallet_year_month(request, datetime.now().year, datetime.now().month)


def wallet_year_month(request, year, month):
    filterArgsByYearMonth = {'year': year, 'month': month}
    wallet_accounts = WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('-type', 'name')
    wallet_deposits = WalletDeposit.objects.filter(**filterArgsByYearMonth).order_by('name')
    wallet_credits = WalletCredit.objects.filter(**filterArgsByYearMonth).order_by('name')
    wallet_incomes = WalletIncome.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
    wallet_expenses = WalletExpense.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
    wallet_houses = WalletHouse.objects.filter(**filterArgsByYearMonth).order_by('name')
    wallet_cars = WalletCar.objects.filter(**filterArgsByYearMonth).order_by('exploitation')

    filterArgsByYearMonthCurrency = {'year': year, 'month': month, 'currency': 'zł'}
    wallet_accounts_sum = WalletAccount.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('value')).get('total_value') or Decimal('0.0')
    wallet_deposits_sum = WalletDeposit.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('value')).get('total_value') or Decimal('0.0')
    wallet_credits_sum = (WalletCredit.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('capital')).get('total_value') or Decimal('0.0')) \
                         + (WalletCredit.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('interest')).get('total_value') or Decimal('0.0')) \
                         + (WalletCredit.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('insurance')).get('total_value') or Decimal('0.0'))
    wallet_incomes_sum = WalletIncome.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('value')).get('total_value') or Decimal('0.0')
    wallet_expenses_sum = WalletExpense.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('value')).get('total_value') or Decimal('0.0')
    # wallet_houses_sum = WalletHouse.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('value')).get('total_value') or Decimal('0.0')
    wallet_cars_sum = WalletCar.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('payment')).get('total_value') or Decimal('0.0')
    wallet_cars_refuelling = WalletCar.objects.filter(**filterArgsByYearMonthCurrency).aggregate(total_value=Sum('refuelling')).get('total_value') or Decimal('0.0')
    wallet_cars_exploitation = WalletCar.objects.filter(**filterArgsByYearMonthCurrency).aggregate(max_value=Max('exploitation'), min_value=Min('exploitation'))
    wallet_cars_exploitation_min = wallet_cars_exploitation.get('min_value') or Decimal('0.0')
    wallet_cars_exploitation_max = wallet_cars_exploitation.get('max_value') or Decimal('0.0')
    wallet_cars_exploitation_distance = wallet_cars_exploitation_max - wallet_cars_exploitation_min
    if wallet_cars_exploitation_distance > 0:
        wallet_cars_refuelling_100km = round(100 * wallet_cars_refuelling / wallet_cars_exploitation_distance, 2)
        wallet_cars_refuelling_avg_price = round(wallet_cars_sum / wallet_cars_refuelling, 2)
    else:
        wallet_cars_refuelling_100km = Decimal('0.0')
        wallet_cars_refuelling_avg_price = Decimal('0.0')

    # for document_wallet in mongoDatabase.wallet.find():
        # json_object = json_util.dumps(document_wallet)
        # print(request.path + ": " + json_object)

    wallet_expenses_json = []
    for wallet_expense_json in wallet_expenses:
        wallet_expenses_json.append({ "key": wallet_expense_json.name, "value": float(wallet_expense_json.value)})

    # print('wallet_accounts_sum=' + str(wallet_accounts_sum) + ' ' +
    #     'wallet_deposits_sum=' + str(wallet_deposits_sum) + ' ' +
    #     'wallet_incomes_sum=' + str(wallet_incomes_sum) + ' ' +
    #     'wallet_expenses_sum=' + str(wallet_expenses_sum) + ' ' +
    #     # 'wallet_houses_sum=' + str(wallet_houses_sum) + ' ' +
    #     'wallet_cars_sum=' + str(wallet_cars_sum) + ' ' +
    #     'wallet_credits_sum=' + str(wallet_credits_sum))

    return render(request, 'app/wallet.html', {
        'year': year,
        'month': month,
        'year_next': int(year)+1 if int(month) == 12 else year,
        'month_next': int(month)+1 if int(month) < 12 else 1,
        'year_prev': int(year)-1 if int(month) == 1 else year,
        'month_prev': int(month)-1 if int(month) > 1 else 12,
        'wallet_accounts': wallet_accounts,
        'wallet_deposits': wallet_deposits,
        'wallet_credits': wallet_credits,
        'wallet_incomes': wallet_incomes,
        'wallet_expenses': wallet_expenses,
        'wallet_expenses_json': json_util.dumps(wallet_expenses_json),
        'wallet_houses': wallet_houses,
        'wallet_cars': wallet_cars,
        'wallet_accounts_sum': wallet_accounts_sum,
        'wallet_deposits_sum': wallet_deposits_sum,
        'wallet_incomes_sum': wallet_incomes_sum,
        'wallet_expenses_sum': wallet_expenses_sum,
        # 'wallet_houses_sum': wallet_houses_sum,
        'wallet_cars_sum': wallet_cars_sum,
        'wallet_cars_refuelling': wallet_cars_refuelling,
        'wallet_cars_exploitation_min': wallet_cars_exploitation_min,
        'wallet_cars_exploitation_max': wallet_cars_exploitation_max,
        'wallet_cars_exploitation_distance': wallet_cars_exploitation_distance,
        'wallet_cars_refuelling_100km': wallet_cars_refuelling_100km,
        'wallet_cars_refuelling_avg_price': wallet_cars_refuelling_avg_price,
        'wallet_credits_sum': wallet_credits_sum,
        'wallet_count_elements': wallet_accounts.count() + wallet_deposits.count() + wallet_credits.count() + wallet_incomes.count() + wallet_expenses.count() + wallet_houses.count() + wallet_cars.count()
    })


def wallet_add(request):
    if request.method == "POST":
        if "/wallet/account/" in request.path:
            form = WalletAccountForm(request.POST)
        elif "/wallet/credit/" in request.path:
            form = WalletCreditForm(request.POST)
        elif "/wallet/deposit/" in request.path:
            form = WalletDepositForm(request.POST)
        elif "/wallet/income/" in request.path:
            form = WalletIncomeForm(request.POST)
        elif "/wallet/expense/" in request.path:
            form = WalletExpenseForm(request.POST)
        elif "/wallet/house/" in request.path:
            form = WalletHouseForm(request.POST)
        elif "/wallet/car/" in request.path:
            form = WalletCarForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            if "/wallet/account/" in request.path:
                json_list = serialize('json', [WalletAccount.objects.get(id=post.id)])
            elif "/wallet/credit/" in request.path:
                json_list = serialize('json', [WalletCredit.objects.get(id=post.id)])
            elif "/wallet/deposit/" in request.path:
                json_list = serialize('json', [WalletDeposit.objects.get(id=post.id)])
            elif "/wallet/income/" in request.path:
                json_list = serialize('json', [WalletIncome.objects.get(id=post.id)])
            elif "/wallet/expense/" in request.path:
                json_list = serialize('json', [WalletExpense.objects.get(id=post.id)])
            elif "/wallet/house/" in request.path:
                json_list = serialize('json', [WalletHouse.objects.get(id=post.id)])
            elif "/wallet/car/" in request.path:
                json_list = serialize('json', [WalletCar.objects.get(id=post.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.insert_one(python_list[0])
            # print(request.path + ": " + json_object + "; result: " + str(result.inserted_id))

            return redirect('wallet')
    else:
        if "/wallet/account/" in request.path:
            form = WalletAccountForm()
            title = 'New wallet account'
        elif "/wallet/credit/" in request.path:
            form = WalletCreditForm()
            title = 'New wallet credit'
        elif "/wallet/deposit/" in request.path:
            form = WalletDepositForm()
            title = 'New wallet deposit'
        elif "/wallet/income/" in request.path:
            form = WalletIncomeForm()
            title = 'New wallet income'
        elif "/wallet/expense/" in request.path:
            form = WalletExpenseForm()
            title = 'New wallet expense'
        elif "/wallet/house/" in request.path:
            form = WalletHouseForm()
            title = 'New wallet house'
        elif "/wallet/car/" in request.path:
            form = WalletCarForm()
            title = 'New wallet car'

    return render(request, 'app/wallet_form.html', {
         'form': form,
         'title':  title,
         'button': 'Add'
    })


def wallet_edit(request, id):
    if "/wallet/account/" in request.path:
        wallet_account = get_object_or_404(WalletAccount, id=id)
    elif "/wallet/credit/" in request.path:
        wallet_credit = get_object_or_404(WalletCredit, id=id)
    elif "/wallet/deposit/" in request.path:
        wallet_deposit = get_object_or_404(WalletDeposit, id=id)
    elif "/wallet/income/" in request.path:
        wallet_income = get_object_or_404(WalletIncome, id=id)
    elif "/wallet/expense/" in request.path:
        wallet_expense = get_object_or_404(WalletExpense, id=id)
    elif "/wallet/house/" in request.path:
        wallet_house = get_object_or_404(WalletHouse, id=id)
    elif "/wallet/car/" in request.path:
        wallet_car = get_object_or_404(WalletCar, id=id)

    if request.method == "POST":
        if "/wallet/account/" in request.path:
            form = WalletAccountForm(request.POST, instance=wallet_account)
        elif "/wallet/credit/" in request.path:
            form = WalletCreditForm(request.POST, instance=wallet_credit)
        elif "/wallet/deposit/" in request.path:
            form = WalletDepositForm(request.POST, instance=wallet_deposit)
        elif "/wallet/income/" in request.path:
            form = WalletIncomeForm(request.POST, instance=wallet_income)
        elif "/wallet/expense/" in request.path:
            form = WalletExpenseForm(request.POST, instance=wallet_expense)
        elif "/wallet/house/" in request.path:
            form = WalletHouseForm(request.POST, instance=wallet_house)
        elif "/wallet/car/" in request.path:
            form = WalletCarForm(request.POST, instance=wallet_car)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            if "/wallet/account/" in request.path:
                json_list = serialize('json', [WalletAccount.objects.get(id=post.id)])
                model = "app.walletaccount"
            elif "/wallet/credit/" in request.path:
                json_list = serialize('json', [WalletCredit.objects.get(id=post.id)])
                model = "app.walletcredit"
            elif "/wallet/deposit/" in request.path:
                json_list = serialize('json', [WalletDeposit.objects.get(id=post.id)])
                model = "app.walletdeposit"
            elif "/wallet/income/" in request.path:
                json_list = serialize('json', [WalletIncome.objects.get(id=post.id)])
                model = "app.walletincome"
            elif "/wallet/expense/" in request.path:
                json_list = serialize('json', [WalletExpense.objects.get(id=post.id)])
                model = "app.walletexpense"
            elif "/wallet/house/" in request.path:
                json_list = serialize('json', [WalletHouse.objects.get(id=post.id)])
                model = "app.wallethouse"
            elif "/wallet/car/" in request.path:
                json_list = serialize('json', [WalletCar.objects.get(id=post.id)])
                model = "app.walletcar"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": post.id, "model": model}, python_list[0], True)
            # print(request.path + ": " + json_object + "; result: " + str(result.matched_count))

            return redirect('wallet')
    else:
        if "/wallet/account/" in request.path:
            form = WalletAccountForm(instance=wallet_account)
            title = 'Edit wallet account'
        elif "/wallet/credit/" in request.path:
            form = WalletCreditForm(instance=wallet_credit)
            title = 'Edit wallet credit'
        elif "/wallet/deposit/" in request.path:
            form = WalletDepositForm(instance=wallet_deposit)
            title = 'Edit wallet deposit'
        elif "/wallet/income/" in request.path:
            form = WalletIncomeForm(instance=wallet_income)
            title = 'Edit wallet income'
        elif "/wallet/expense/" in request.path:
            form = WalletExpenseForm(instance=wallet_expense)
            title = 'Edit wallet expense'
        elif "/wallet/house/" in request.path:
            form = WalletHouseForm(instance=wallet_house)
            title = 'Edit wallet house'
        elif "/wallet/car/" in request.path:
            form = WalletCarForm(instance=wallet_car)
            title = 'Edit wallet car'

    return render(request, 'app/wallet_form.html', {'form': form,
                                                 'title': title,
                                                 'button': 'Save',
                                                 'id': id})


def wallet_remove(request, id):
    if "/wallet/account/" in request.path:
        wallet_account = get_object_or_404(WalletAccount, id=id)
        WalletAccount.objects.get(id=id).delete()
    elif "/wallet/credit/" in request.path:
        wallet_credit = get_object_or_404(WalletCredit, id=id)
        WalletCredit.objects.get(id=id).delete()
    elif "/wallet/deposit/" in request.path:
        wallet_deposit = get_object_or_404(WalletDeposit, id=id)
        WalletDeposit.objects.get(id=id).delete()
    elif "/wallet/income/" in request.path:
        wallet_income = get_object_or_404(WalletIncome, id=id)
        WalletIncome.objects.get(id=id).delete()
    elif "/wallet/expense/" in request.path:
        wallet_expense = get_object_or_404(WalletExpense, id=id)
        WalletExpense.objects.get(id=id).delete()
    elif "/wallet/house/" in request.path:
        wallet_house= get_object_or_404(WalletHouse, id=id)
        WalletHouse.objects.get(id=id).delete()
    elif "/wallet/car/" in request.path:
        wallet_car = get_object_or_404(WalletCar, id=id)
        WalletCar.objects.get(id=id).delete()

    if "/wallet/account/" in request.path:
        json_list = serialize('json', [wallet_account])
        model = "app.walletaccount"
    elif "/wallet/credit/" in request.path:
        json_list = serialize('json', [wallet_credit])
        model = "app.walletcredit"
    elif "/wallet/deposit/" in request.path:
        json_list = serialize('json', [wallet_deposit])
        model = "app.walletdeposit"
    elif "/wallet/income/" in request.path:
        json_list = serialize('json', [wallet_income])
        model = "app.walletincome"
    elif "/wallet/expense/" in request.path:
        json_list = serialize('json', [wallet_expense])
        model = "app.walletexpense"
    elif "/wallet/house/" in request.path:
        json_list = serialize('json', [wallet_house])
        model = "app.wallethouse"
    elif "/wallet/car/" in request.path:
        json_list = serialize('json', [wallet_car])
        model = "app.walletcar"
    python_list = json_util.loads(json_list)
    json_object = json_util.dumps(python_list[0])
    result = mongoDatabase.wallet.delete_one({"pk": int(id), "model": model})
    # print(request.path + ": " + json_object + "; result: " + str(result.deleted_count))

    return redirect('wallet')