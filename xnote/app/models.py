from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


def current_year():
    now = datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second
    return now.year


def current_month():
    now = datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second
    return now.month


PREDEFINED_COLORS = (
    ('red', 'Red'),
    ('orange', 'Orange'),
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
    ('grey', 'Grey'),
    ('brown', 'Brown'),
    ('yellow', 'Yellow'),
    ('magenta', 'Magenta'),
)


REMINDER_REPEAT = (
    ('1d', 'Every day'),
    ('7d', 'Every week'),
    ('14d', 'Every 2 weeks'),
    ('30d', 'Every 30 days'),
    ('1m', 'Every month'),
    ('2m', 'Every 2 months'),
    ('3m', 'Every 3 months'),
    ('1y', 'Every year'),
)


REMINDER_PRIORITY = (
    ('low', 'Low'),
    ('normal', 'Normal'),
    ('high', 'High'),
)


LOG_TYPE_CHOICES = (
    ('wallet', 'Wallet'),
    ('calendar', 'Calendar'),
    ('reminder', 'Reminder'),
    ('note', 'Note'),
)


WALLET_YEAR_CHOICES = [(i,i) for i in range(2010, 2100)]

WALLET_MONTH_CHOICES = [(i,i) for i in range(1, 13)]

WALLET_ACCOUNT_TYPE_CHOICES = (
    ('wallet', 'Wallet'),
    ('bank account', 'Bank account'),
    ('mobile account', 'Mobile account'),
)

WALLET_INCOME_TYPE_CHOICES = (
    ('regular', 'Regular'),
    ('casual', 'Casual')
)

WALLET_EXPENSE_TYPE_CHOICES = (
    ('life', 'Life'),
    ('tickets', 'Ticket'),
    ('house rent', 'House rent'),
)

WALLET_CURRENCY = (
    ('zł', 'zł'),
    ('eu', 'eu'),
    ('$', '$'),
    ('gbp', 'gbp'),
    ('kc', 'kc'),
)


class Token(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    token = models.JSONField()


class ReminderGroup(models.Model):
    color = models.CharField(max_length=32, null=False, blank=False, choices=PREDEFINED_COLORS, default='orange')
    name = models.CharField(max_length=64, null=False, blank=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or ''


class Reminder(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    when = models.DateTimeField(auto_now=False, null=True, blank=True)
    repeat = models.CharField(max_length=32, null=True, blank=True, choices=REMINDER_REPEAT)
    priority = models.CharField(max_length=32, null=False, blank=False, choices=REMINDER_PRIORITY, default='normal')
    group = models.ForeignKey(ReminderGroup, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or ''


class Log(models.Model):
    type = models.CharField(max_length=32, null=False, blank=False, choices=LOG_TYPE_CHOICES, default='note')
    info = models.CharField(max_length=64, null=False, blank=False)
    json = models.TextField(max_length=512, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.info or ''


class WalletAccount(models.Model):
    type = models.CharField(max_length=32, null=False, blank=False, choices=WALLET_ACCOUNT_TYPE_CHOICES, default='wallet')
    name = models.CharField(max_length=64, null=False, blank=False)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False, default=current_year(), choices=WALLET_YEAR_CHOICES)
    month = models.IntegerField(null=False, blank=False, default=current_month(), choices=WALLET_MONTH_CHOICES)
    currency = models.CharField(max_length=8, null=False, blank=False, choices=WALLET_CURRENCY, default='zł')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or ''


class WalletCredit(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    rate = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    balance = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    interest = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    capital = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    insurance = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False, default=current_year(), choices=WALLET_YEAR_CHOICES)
    month = models.IntegerField(null=False, blank=False, default=current_month(), choices=WALLET_MONTH_CHOICES)
    currency = models.CharField(max_length=8, null=False, blank=False, choices=WALLET_CURRENCY, default='zł')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or ''


class WalletDeposit(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    rate = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False, default=current_year(), choices=WALLET_YEAR_CHOICES)
    month = models.IntegerField(null=False, blank=False, default=current_month(), choices=WALLET_MONTH_CHOICES)
    currency = models.CharField(max_length=8, null=False, blank=False, choices=WALLET_CURRENCY, default='zł')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or ''


class WalletIncome(models.Model):
    type = models.CharField(max_length=32, null=False, blank=False, choices=WALLET_INCOME_TYPE_CHOICES, default='regular')
    name = models.CharField(max_length=64, null=False, blank=False)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False, default=current_year(), choices=WALLET_YEAR_CHOICES)
    month = models.IntegerField(null=False, blank=False, default=current_month(), choices=WALLET_MONTH_CHOICES)
    currency = models.CharField(max_length=8, null=False, blank=False, choices=WALLET_CURRENCY, default='zł')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or ''


class WalletExpense(models.Model):
    type = models.CharField(max_length=32, null=False, blank=False, choices=WALLET_EXPENSE_TYPE_CHOICES, default='life')
    name = models.CharField(max_length=64, null=False, blank=False)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False, default=current_year(), choices=WALLET_YEAR_CHOICES)
    month = models.IntegerField(null=False, blank=False, default=current_month(), choices=WALLET_MONTH_CHOICES)
    currency = models.CharField(max_length=8, null=False, blank=False, choices=WALLET_CURRENCY, default='zł')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or ''


class WalletHouse(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    value = models.DecimalField(max_digits=20, decimal_places=3, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False, default=current_year(), choices=WALLET_YEAR_CHOICES)
    month = models.IntegerField(null=False, blank=False, default=current_month(), choices=WALLET_MONTH_CHOICES)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or ''


class WalletCar(models.Model):
    car = models.CharField(max_length=64, null=False, blank=False)
    exploitation = models.IntegerField(null=False, blank=False)
    payment = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    refuelling = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False, default=current_year(), choices=WALLET_YEAR_CHOICES)
    month = models.IntegerField(null=False, blank=False, default=current_month(), choices=WALLET_MONTH_CHOICES)
    currency = models.CharField(max_length=8, null=False, blank=False, choices=WALLET_CURRENCY, default='zł')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.car or ''
