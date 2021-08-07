from datetime import datetime

from django import forms

from .models import Log, WalletAccount, WalletCredit, WalletDeposit, WalletIncome, WalletExpense, WalletCar, \
    WalletHouse, Reminder, ReminderGroup


class ReminderGroupForm(forms.ModelForm):
    class Meta:
        model = ReminderGroup
        ordering = ["name"]
        fields = ['color', 'name']


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        ordering = ["name"]
        fields = ['name', 'when', 'group', 'repeat', 'priority']

    def __init__(self, *args, **kwargs):
        super(ReminderForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = self.fields['group'].queryset.order_by('name')


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ['type', 'info', 'json']


class WalletAccountForm(forms.ModelForm):
    class Meta:
        model = WalletAccount
        fields = ['type', 'name', 'value', 'currency', 'month', 'year']


class WalletCreditForm(forms.ModelForm):
    class Meta:
        model = WalletCredit
        fields = ['name', 'value', 'currency', 'rate', 'balance', 'interest', 'insurance', 'capital', 'month', 'year']


class WalletDepositForm(forms.ModelForm):
    class Meta:
        model = WalletDeposit
        fields = ['name', 'value', 'currency', 'rate', 'month', 'year']


class WalletIncomeForm(forms.ModelForm):
    class Meta:
        model = WalletIncome
        fields = ['type', 'name', 'value', 'currency', 'month', 'year']


class WalletExpenseForm(forms.ModelForm):
    class Meta:
        model = WalletExpense
        fields = ['type', 'name', 'value', 'currency', 'month', 'year']


class WalletHouseForm(forms.ModelForm):
    class Meta:
        model = WalletHouse
        fields = ['name', 'value', 'month', 'year']


class WalletCarForm(forms.ModelForm):
    class Meta:
        model = WalletCar
        fields = ['car', 'exploitation', 'payment', 'currency', 'refuelling', 'month', 'year']


class WalletWizardShoppingForm(forms.Form):
    value = forms.DecimalField(max_digits=20, decimal_places=2)
    from_account = forms.ChoiceField()
    for_expense = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(WalletWizardShoppingForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].choices = self.list_accounts()
        self.fields['for_expense'].choices = self.list_expenses()

    def list_accounts(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletAccount.name, walletAccount.name) for walletAccount in
        WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )

    def list_expenses(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletExpense.name, walletExpense.name) for walletExpense in
        WalletExpense.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )



class WalletWizardRefuellingForm(forms.Form):
    value = forms.DecimalField(max_digits=20, decimal_places=2)
    from_account = forms.ChoiceField()
    for_car = forms.ChoiceField()
    refuelling = forms.DecimalField(max_digits=20, decimal_places=2)
    exploitation = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(WalletWizardRefuellingForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].choices = self.list_accounts()
        self.fields['for_car'].choices = self.list_cars()

    def list_accounts(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletAccount.name, walletAccount.name) for walletAccount in
        WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )

    def list_cars(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return set(
            (walletCar.car, walletCar.car) for walletCar in WalletCar.objects.filter(**filterArgsByYearMonth).order_by('car')
        )


class WalletWizardIncomingForm(forms.Form):
    value = forms.DecimalField(max_digits=20, decimal_places=2)
    from_income = forms.ChoiceField()
    for_account = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(WalletWizardIncomingForm, self).__init__(*args, **kwargs)
        self.fields['from_income'].choices = self.list_incomes()
        self.fields['for_account'].choices = self.list_accounts()

    def list_accounts(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletAccount.name, walletAccount.name) for walletAccount in
        WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )

    def list_incomes(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletIncome.name, walletIncome.name) for walletIncome in
        WalletIncome.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )

class WalletWizardTransferringAccountsForm(forms.Form):
    value = forms.DecimalField(max_digits=20, decimal_places=2)
    from_account = forms.ChoiceField()
    to_account = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(WalletWizardTransferringAccountsForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].choices = self.list_accounts()
        self.fields['to_account'].choices = self.list_accounts()

    def list_accounts(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletAccount.name, walletAccount.name) for walletAccount in
        WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )

class WalletWizardCurrencyExchangeForm(forms.Form):
    from_account = forms.ChoiceField()
    to_account = forms.ChoiceField()
    value = forms.DecimalField(max_digits=20, decimal_places=2)
    operation = forms.ChoiceField()
    exchange_rate = forms.DecimalField(max_digits=20, decimal_places=2)
    calculated_value = forms.DecimalField(max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(WalletWizardCurrencyExchangeForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].choices = self.list_accounts()
        self.fields['to_account'].choices = self.list_accounts()
        self.fields['operation'].choices = [('purchase', 'purchase'), ('sale', 'sale')];

    def list_accounts(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletAccount.name, walletAccount.name) for walletAccount in
            WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )

class WalletWizardCreditingForm(forms.Form):
    capital = forms.DecimalField(max_digits=20, decimal_places=2)
    interest = forms.DecimalField(max_digits=20, decimal_places=2)
    insurance = forms.DecimalField(max_digits=20, decimal_places=2)
    from_account = forms.ChoiceField()
    to_credit = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(WalletWizardCreditingForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].choices = self.list_accounts()
        self.fields['to_credit'].choices = self.list_credits()

    def list_accounts(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletAccount.name, walletAccount.name) for walletAccount in
        WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )

    def list_credits(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletCredit.name, walletCredit.name) for walletCredit in
        WalletCredit.objects.filter(**filterArgsByYearMonth).order_by('name')
        )

class WalletWizardDepositingForm(forms.Form):
    value = forms.DecimalField(max_digits=20, decimal_places=2)
    from_account = forms.ChoiceField()
    to_deposit = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(WalletWizardDepositingForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].choices = self.list_accounts()
        self.fields['to_deposit'].choices = self.list_deposits()

    def list_accounts(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletAccount.name, walletAccount.name) for walletAccount in
        WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )

    def list_deposits(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletDeposit.name, walletDeposit.name) for walletDeposit in
        WalletDeposit.objects.filter(**filterArgsByYearMonth).order_by('name')
        )


class WalletWizardTransferringAccountDepositForm(forms.Form):
    value = forms.DecimalField(max_digits=20, decimal_places=2)
    from_deposit = forms.ChoiceField()
    to_account = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(WalletWizardTransferringAccountDepositForm, self).__init__(*args, **kwargs)
        self.fields['from_deposit'].choices = self.list_deposits()
        self.fields['to_account'].choices = self.list_accounts()

    def list_accounts(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletAccount.name, walletAccount.name) for walletAccount in
        WalletAccount.objects.filter(**filterArgsByYearMonth).order_by('type', 'name')
        )

    def list_deposits(self):
        now = datetime.now()
        filterArgsByYearMonth = {'year': now.year, 'month': now.month}
        return (
            (walletDeposit.name, walletDeposit.name) for walletDeposit in
        WalletDeposit.objects.filter(**filterArgsByYearMonth).order_by('name')
        )
