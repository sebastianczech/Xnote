from django.urls import path, re_path

from . import views, views_note, views_reminder, views_wallet, views_log, views_calendar, \
    views_wallet_generator, views_wallet_wizard, views_wallet_analytics, views_wallet_car, views_search, \
    views_wallet_rent

urlpatterns = [
    path('', views.index, name='index'),
    # re_path(r'^$', views.index, name='index'),

    re_path(r'^wallet/$', views_wallet.wallet, name='wallet'),
    re_path(r'^wallet/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views_wallet.wallet_year_month, name='wallet_year_month'),
    re_path(r'^wallet/analytics/$', views_wallet_analytics.wallet_analytics_year_month, name='wallet_analytics_year_month'),
    re_path(r'^wallet/car/$', views_wallet_car.wallet_car_year_month, name='wallet_car_year_month'),
    re_path(r'^wallet/rent/$', views_wallet_rent.wallet_rent_year_month, name='wallet_rent_year_month'),
    re_path(r'^wallet/generator/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views_wallet_generator.wallet_generator_year_month, name='wallet_generator_year_month'),
    re_path(r'^wallet/clear/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views_wallet_generator.wallet_clear_year_month, name='wallet_clear_year_month'),
    re_path(r'^wallet/wizard/shopping/$', views_wallet_wizard.wallet_wizard_shopping, name='wallet_wizard_shopping'),
    re_path(r'^wallet/wizard/refuelling/$', views_wallet_wizard.wallet_wizard_refuelling, name='wallet_wizard_refuelling'),
    re_path(r'^wallet/wizard/account_transferring/$', views_wallet_wizard.wallet_wizard_account_transferring,
        name='wallet_wizard_account_transferring'),
    re_path(r'^wallet/wizard/wallet_wizard_crediting/$', views_wallet_wizard.wallet_wizard_crediting,
        name='wallet_wizard_crediting'),
    re_path(r'^wallet/wizard/deposit_transferring/$', views_wallet_wizard.wallet_wizard_deposit_transferring,
        name='wallet_wizard_deposit_transferring'),
    re_path(r'^wallet/wizard/currency_exchange/$', views_wallet_wizard.wallet_wizard_currency_exchange,
        name='wallet_wizard_currency_exchange'),
    re_path(r'^wallet/wizard/depositing/$', views_wallet_wizard.wallet_wizard_depositing, name='wallet_wizard_depositing'),
    re_path(r'^wallet/wizard/incoming/$', views_wallet_wizard.wallet_wizard_incoming, name='wallet_wizard_incoming'),
    re_path(r'^wallet/account/add/$', views_wallet.wallet_add, name='wallet_account_add'),
    re_path(r'^wallet/account/(?P<id>[0-9]+)/edit$', views_wallet.wallet_edit, name='wallet_account_edit'),
    re_path(r'^wallet/account/(?P<id>[0-9]+)/remove', views_wallet.wallet_remove, name='wallet_account_remove'),
    re_path(r'^wallet/credit/add/$', views_wallet.wallet_add, name='wallet_credit_add'),
    re_path(r'^wallet/credit/(?P<id>[0-9]+)/edit$', views_wallet.wallet_edit, name='wallet_credit_edit'),
    re_path(r'^wallet/credit/(?P<id>[0-9]+)/remove', views_wallet.wallet_remove, name='wallet_credit_remove'),
    re_path(r'^wallet/deposit/add/$', views_wallet.wallet_add, name='wallet_deposit_add'),
    re_path(r'^wallet/deposit/(?P<id>[0-9]+)/edit$', views_wallet.wallet_edit, name='wallet_deposit_edit'),
    re_path(r'^wallet/deposit/(?P<id>[0-9]+)/remove', views_wallet.wallet_remove, name='wallet_deposit_remove'),
    re_path(r'^wallet/income/add/$', views_wallet.wallet_add, name='wallet_income_add'),
    re_path(r'^wallet/income/(?P<id>[0-9]+)/edit$', views_wallet.wallet_edit, name='wallet_income_edit'),
    re_path(r'^wallet/income/(?P<id>[0-9]+)/remove', views_wallet.wallet_remove, name='wallet_income_remove'),
    re_path(r'^wallet/expense/add/$', views_wallet.wallet_add, name='wallet_expense_add'),
    re_path(r'^wallet/expense/(?P<id>[0-9]+)/edit$', views_wallet.wallet_edit, name='wallet_expense_edit'),
    re_path(r'^wallet/expense/(?P<id>[0-9]+)/remove', views_wallet.wallet_remove, name='wallet_expense_remove'),
    re_path(r'^wallet/house/add/$', views_wallet.wallet_add, name='wallet_house_add'),
    re_path(r'^wallet/house/(?P<id>[0-9]+)/edit$', views_wallet.wallet_edit, name='wallet_house_edit'),
    re_path(r'^wallet/house/(?P<id>[0-9]+)/remove', views_wallet.wallet_remove, name='wallet_house_remove'),
    re_path(r'^wallet/car/add/$', views_wallet.wallet_add, name='wallet_car_add'),
    re_path(r'^wallet/car/(?P<id>[0-9]+)/edit$', views_wallet.wallet_edit, name='wallet_car_edit'),
    re_path(r'^wallet/car/(?P<id>[0-9]+)/remove', views_wallet.wallet_remove, name='wallet_car_remove'),

    re_path(r'^calendar/$', views_calendar.calendar, name='calendar'),

    re_path(r'^reminder/$', views_reminder.reminder, name='reminder'),
    re_path(r'^reminder/add/$', views_reminder.reminder_add, name='reminder_add'),
    re_path(r'^reminder/time/(?P<time>[\w]+)$', views_reminder.reminder_in_time, name='reminder_in_time'),
    re_path(r'^reminder/(?P<id>[\w\-]+)/$', views_reminder.reminder_in_group, name='reminder_in_group'),
    re_path(r'^reminder/(?P<id>[0-9]+)/edit$', views_reminder.reminder_edit, name='reminder_edit'),
    re_path(r'^reminder/(?P<id>[0-9]+)/remove', views_reminder.reminder_remove, name='reminder_remove'),
    re_path(r'^reminder/(?P<id>[0-9]+)/calendar', views_reminder.reminder_add_to_calendar, name='reminder_add_to_calendar'),
    re_path(r'^reminder/group/add/$', views_reminder.reminder_group_add, name='reminder_group_add'),
    re_path(r'^reminder/group/(?P<id>[0-9]+)/edit$', views_reminder.reminder_group_edit, name='reminder_group_edit'),
    re_path(r'^reminder/group/(?P<id>[0-9]+)/remove', views_reminder.reminder_group_remove, name='reminder_group_remove'),

    re_path(r'^note/$', views_note.note, name='note'),

    re_path(r'^log/$', views_log.log, name='log'),
    re_path(r'^log/add/$', views_log.log_add, name='log_add'),
    re_path(r'^log/(?P<id>[0-9]+)/$', views_log.log_detail, name='log_detail'),
    re_path(r'^log/(?P<id>[0-9]+)/edit$', views_log.log_edit, name='log_edit'),
    re_path(r'^log/(?P<id>[0-9]+)/remove', views_log.log_remove, name='log_remove'),

    re_path(r'^search/$', views_search.search, name='search'),
]