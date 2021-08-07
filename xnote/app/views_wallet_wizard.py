from datetime import datetime

from bson import json_util
from django.core.serializers import serialize
from django.shortcuts import render, redirect

from . import mongoDatabase
from .forms import WalletWizardShoppingForm, WalletWizardRefuellingForm, WalletWizardIncomingForm, \
    WalletWizardTransferringAccountsForm, WalletWizardTransferringAccountDepositForm, WalletWizardDepositingForm, \
    WalletWizardCreditingForm, WalletWizardCurrencyExchangeForm
from .models import WalletAccount, WalletExpense, WalletCar, Log, WalletIncome, WalletDeposit, WalletCredit


def wallet_wizard_shopping(request):
    if request.method == 'POST':
        form = WalletWizardShoppingForm(request.POST)
        if form.is_valid():
            # print("Value: " + str(form.cleaned_data['value']) + ", " +
            #       "from account: " + str(form.cleaned_data['from_account']) + ", " +
            #       "for expense: " + str(form.cleaned_data['for_expense']))

            walletAccount = WalletAccount.objects.get(name=str(form.cleaned_data['from_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccount.value = walletAccount.value - form.cleaned_data['value']
            walletAccount.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccount.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccount.id, "model": model}, python_list[0], True)
            # print(request.path + ": " + json_object + "; result: " + str(result.matched_count))

            walletExpense = WalletExpense.objects.get(name=str(form.cleaned_data['for_expense']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletExpense.value = walletExpense.value + form.cleaned_data['value']
            walletExpense.save()

            json_list = serialize('json', [WalletExpense.objects.get(id=walletExpense.id)])
            model = "app.walletexpense"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletExpense.id, "model": model}, python_list[0], True)
            # print(request.path + ": " + json_object + "; result: " + str(result.matched_count))

            json = {
                    "value": str(form.cleaned_data['value']),
                    "from_account": str(form.cleaned_data['from_account']),
                    "for_expense": str(form.cleaned_data['for_expense'])
            }

            log = Log.objects.create(type='wallet',
                                     info='Wizard shopping',
                                     json=json_util.dumps(json).replace(",", ",\n"),
                                     user=request.user)

            json_list = serialize('json', [Log.objects.get(id=log.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.insert_one(python_list[0])

            return redirect('wallet')
    else:
        form = WalletWizardShoppingForm()

    return render(request, 'app/wallet_form.html', {
        'form': form,
        'title': 'Wallet wizard shopping',
        'button': 'Create'
    })


def wallet_wizard_refuelling(request):
    if request.method == 'POST':
        form = WalletWizardRefuellingForm(request.POST)
        if form.is_valid():
            # print("Value: " + str(form.cleaned_data['value']) + ", " +
            #       "from account: " + str(form.cleaned_data['from_account']) + ", " +
            #       "for car: " + str(form.cleaned_data['for_car']) + ", " +
            #       "refuelling: " + str(form.cleaned_data['refuelling']) + ", " +
            #       "exploitation: " + str(form.cleaned_data['exploitation']))

            walletAccount = WalletAccount.objects.get(name=str(form.cleaned_data['from_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccount.value = walletAccount.value - form.cleaned_data['value']
            walletAccount.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccount.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccount.id, "model": model}, python_list[0], True)
            # print(request.path + ": " + json_object + "; result: " + str(result.matched_count))

            walletCar = WalletCar.objects.create(car=str(form.cleaned_data['for_car']),
                                     exploitation=form.cleaned_data['exploitation'],
                                     refuelling=form.cleaned_data['refuelling'],
                                     payment=form.cleaned_data['value'],
                                     year=datetime.now().year,
                                     month=datetime.now().month,
                                     user = request.user)

            json_list = serialize('json', [WalletCar.objects.get(id=walletCar.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.insert_one(python_list[0])
            # print(request.path + ": " + json_object + "; result: " + str(result.inserted_id))

            json = {
                "value": str(form.cleaned_data['value']),
                "from_account": str(form.cleaned_data['from_account']),
                "for_car": str(form.cleaned_data['for_car']),
                "exploitation": str(form.cleaned_data['exploitation']),
                "refuelling": str(form.cleaned_data['refuelling'])
            }

            log = Log.objects.create(type='wallet',
                                     info='Wizard refuelling',
                                     json=json_util.dumps(json).replace(",", ",\n"),
                                     user=request.user)

            json_list = serialize('json', [Log.objects.get(id=log.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.insert_one(python_list[0])

            return redirect('wallet')
    else:
        form = WalletWizardRefuellingForm()

    return render(request, 'app/wallet_form.html', {
        'form': form,
        'title': 'Wallet wizard refuelling',
        'button': 'Create'
    })


def wallet_wizard_account_transferring(request):
    if request.method == 'POST':
        form = WalletWizardTransferringAccountsForm(request.POST)
        if form.is_valid():
            walletAccountFrom = WalletAccount.objects.get(name=str(form.cleaned_data['from_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccountFrom.value = walletAccountFrom.value - form.cleaned_data['value']
            walletAccountFrom.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccountFrom.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccountFrom.id, "model": model}, python_list[0], True)

            walletAccountTo = WalletAccount.objects.get(name=str(form.cleaned_data['to_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccountTo.value = walletAccountTo.value + form.cleaned_data['value']
            walletAccountTo.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccountTo.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccountTo.id, "model": model}, python_list[0], True)

            json = {
                "value": str(form.cleaned_data['value']),
                "from_account": str(form.cleaned_data['from_account']),
                "to_account": str(form.cleaned_data['to_account'])
            }

            log = Log.objects.create(type='wallet',
                                     info='Wizard account transferring between accounts',
                                     json=json_util.dumps(json).replace(",", ",\n"),
                                     user=request.user)

            json_list = serialize('json', [Log.objects.get(id=log.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.insert_one(python_list[0])

            return redirect('wallet')
    else:
        form = WalletWizardTransferringAccountsForm()

    return render(request, 'app/wallet_form.html', {
            'form': form,
            'title': 'Wallet wizard transfer between accounts',
            'button': 'Create'
        })

def wallet_wizard_crediting(request):
    if request.method == 'POST':
        form = WalletWizardCreditingForm(request.POST)
        if form.is_valid():
            walletAccountFrom = WalletAccount.objects.get(name=str(form.cleaned_data['from_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccountFrom.value = walletAccountFrom.value - form.cleaned_data['capital'] \
                                      - form.cleaned_data['interest'] - form.cleaned_data['insurance']
            walletAccountFrom.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccountFrom.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccountFrom.id, "model": model}, python_list[0], True)

            walletCreditTo = WalletCredit.objects.get(name=str(form.cleaned_data['to_credit']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletCreditTo.capital = walletCreditTo.capital + form.cleaned_data['capital']
            walletCreditTo.interest = walletCreditTo.interest + form.cleaned_data['interest']
            walletCreditTo.insurance = walletCreditTo.insurance + form.cleaned_data['insurance']
            walletCreditTo.balance = walletCreditTo.balance - form.cleaned_data['capital']
            walletCreditTo.save()

            json_list = serialize('json', [WalletCredit.objects.get(id=walletCreditTo.id)])
            model = "app.walletcredit"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletCreditTo.id, "model": model}, python_list[0], True)

            json = {
                "capital": str(form.cleaned_data['capital']),
                "interest": str(form.cleaned_data['interest']),
                "insurance": str(form.cleaned_data['insurance']),
                "from_account": str(form.cleaned_data['from_account']),
                "to_credit": str(form.cleaned_data['to_credit'])
            }

            log = Log.objects.create(type='wallet',
                                     info='Wizard crediting from account to credit',
                                     json=json_util.dumps(json).replace(",", ",\n"),
                                     user=request.user)

            json_list = serialize('json', [Log.objects.get(id=log.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.insert_one(python_list[0])

            return redirect('wallet')
    else:
        form = WalletWizardCreditingForm()

    return render(request, 'app/wallet_form.html', {
            'form': form,
            'title': 'Wallet wizard crediting',
            'button': 'Create'
        })

def wallet_wizard_currency_exchange(request):
    if request.method == 'POST':
        form = WalletWizardCurrencyExchangeForm(request.POST)
        if form.is_valid():
            walletAccountFrom = WalletAccount.objects.get(name=str(form.cleaned_data['from_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccountFrom.value = walletAccountFrom.value - form.cleaned_data['value']
            walletAccountFrom.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccountFrom.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccountFrom.id, "model": model}, python_list[0], True)

            walletAccountTo = WalletAccount.objects.get(name=str(form.cleaned_data['to_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccountTo.value = walletAccountTo.value + form.cleaned_data['calculated_value']
            walletAccountTo.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccountTo.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccountTo.id, "model": model}, python_list[0], True)

            json = {
                "value": str(form.cleaned_data['value']),
                "operation": str(form.cleaned_data['operation']),
                "exchange_rate": str(form.cleaned_data['exchange_rate']),
                "value": str(form.cleaned_data['calculated_value']),
                "from_account": str(form.cleaned_data['from_account']),
                "to_account": str(form.cleaned_data['to_account'])
            }

            log = Log.objects.create(type='wallet',
                                     info='Wizard currency exchange',
                                     json=json_util.dumps(json).replace(",", ",\n"),
                                     user=request.user)

            json_list = serialize('json', [Log.objects.get(id=log.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.insert_one(python_list[0])

            return redirect('wallet')
    else:
        form = WalletWizardCurrencyExchangeForm()
    return render(request, 'app/wallet_form.html', {
            'form': form,
            'title': 'Wallet wizard currency exchange',
            'button': 'Exchange'
        })

def wallet_wizard_deposit_transferring(request):
    if request.method == 'POST':
        form = WalletWizardTransferringAccountDepositForm(request.POST)
        if form.is_valid():
            walletDeposit = WalletDeposit.objects.get(name=str(form.cleaned_data['from_deposit']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletDeposit.value = walletDeposit.value - form.cleaned_data['value']
            walletDeposit.save()

            json_list = serialize('json', [WalletDeposit.objects.get(id=walletDeposit.id)])
            model = "app.walletdeposit"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletDeposit.id, "model": model}, python_list[0], True)

            walletAccount = WalletAccount.objects.get(name=str(form.cleaned_data['to_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccount.value = walletAccount.value + form.cleaned_data['value']
            walletAccount.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccount.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccount.id, "model": model}, python_list[0], True)

            json = {
                "value": str(form.cleaned_data['value']),
                "from_deposit": str(form.cleaned_data['from_deposit']),
                "to_account": str(form.cleaned_data['to_account'])
            }

            log = Log.objects.create(type='wallet',
                                     info='Wizard deposit transferring to account',
                                     json=json_util.dumps(json).replace(",", ",\n"),
                                     user=request.user)

            json_list = serialize('json', [Log.objects.get(id=log.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.insert_one(python_list[0])

            return redirect('wallet')
    else:
        form = WalletWizardTransferringAccountDepositForm()

    return render(request, 'app/wallet_form.html', {
            'form': form,
            'title': 'Wallet wizard transfer between account and deposit',
            'button': 'Create'
        })


def wallet_wizard_depositing(request):
    if request.method == 'POST':
        form = WalletWizardDepositingForm(request.POST)
        if form.is_valid():
            walletDeposit = WalletDeposit.objects.get(name=str(form.cleaned_data['to_deposit']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletDeposit.value = walletDeposit.value + form.cleaned_data['value']
            walletDeposit.save()

            json_list = serialize('json', [WalletDeposit.objects.get(id=walletDeposit.id)])
            model = "app.walletdeposit"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletDeposit.id, "model": model}, python_list[0], True)

            walletAccount = WalletAccount.objects.get(name=str(form.cleaned_data['from_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccount.value = walletAccount.value - form.cleaned_data['value']
            walletAccount.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccount.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccount.id, "model": model}, python_list[0], True)

            json = {
                "value": str(form.cleaned_data['value']),
                "from_account": str(form.cleaned_data['from_account']),
                "to_deposit": str(form.cleaned_data['to_deposit'])
            }

            log = Log.objects.create(type='wallet',
                                     info='Wizard depositing money',
                                     json=json_util.dumps(json).replace(",", ",\n"),
                                     user=request.user)

            json_list = serialize('json', [Log.objects.get(id=log.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.insert_one(python_list[0])

            return redirect('wallet')
    else:
        form = WalletWizardDepositingForm()

    return render(request, 'app/wallet_form.html', {
            'form': form,
            'title': 'Wallet wizard money depositing',
            'button': 'Create'
        })


def wallet_wizard_incoming(request):
    if request.method == 'POST':
        form = WalletWizardIncomingForm(request.POST)
        if form.is_valid():
            walletIncome = WalletIncome.objects.get(name=str(form.cleaned_data['from_income']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletIncome.value = walletIncome.value + form.cleaned_data['value']
            walletIncome.save()

            json_list = serialize('json', [WalletIncome.objects.get(id=walletIncome.id)])
            model = "app.walletincome"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletIncome.id, "model": model}, python_list[0], True)

            walletAccount = WalletAccount.objects.get(name=str(form.cleaned_data['for_account']),
                                                      year=datetime.now().year,
                                                      month=datetime.now().month)
            walletAccount.value = walletAccount.value + form.cleaned_data['value']
            walletAccount.save()

            json_list = serialize('json', [WalletAccount.objects.get(id=walletAccount.id)])
            model = "app.walletaccount"
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.wallet.replace_one({"pk": walletAccount.id, "model": model}, python_list[0], True)

            json = {
                "value": str(form.cleaned_data['value']),
                "from_income": str(form.cleaned_data['from_income']),
                "for_account": str(form.cleaned_data['for_account'])
            }

            log = Log.objects.create(type='wallet',
                                     info='Wizard incoming money',
                                     json=json_util.dumps(json).replace(",", ",\n"),
                                     user=request.user)

            json_list = serialize('json', [Log.objects.get(id=log.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.insert_one(python_list[0])

            return redirect('wallet')
    else:
        form = WalletWizardIncomingForm()

    return render(request, 'app/wallet_form.html', {
            'form': form,
            'title': 'Wallet wizard incoming money',
            'button': 'Create'
        })