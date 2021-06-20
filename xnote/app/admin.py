from django.contrib import admin

from .models import Token, Log, Reminder, ReminderGroup, WalletAccount, WalletCredit, WalletDeposit, WalletExpense

admin.site.register(Token)
admin.site.register(Log)
admin.site.register(Reminder)
admin.site.register(ReminderGroup)
admin.site.register(WalletAccount)
admin.site.register(WalletCredit)
admin.site.register(WalletDeposit)
admin.site.register(WalletExpense)
