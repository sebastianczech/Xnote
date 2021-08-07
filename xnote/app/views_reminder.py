from datetime import datetime, timedelta

from bson import json_util
from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from monthdelta import monthdelta

from . import mongoDatabase, api_google
from .forms import ReminderForm, ReminderGroupForm
from .models import Reminder, ReminderGroup


def reminder(request):
    reminders_groups = ReminderGroup.objects.all().order_by('name')
    reminders = Reminder.objects.all().order_by('-name')
    # paginator = Paginator(reminders_all, 128)
    #
    # page = request.GET.get('page')
    # try:
    #     reminders = paginator.page(page)
    # except PageNotAnInteger:
    #     reminders = paginator.page(1)
    # except EmptyPage:
    #     reminders = paginator.page(paginator.num_pages)
    return render(request, 'app/reminder.html', { 'reminders' : reminders,
                                                  'reminders_groups': reminders_groups })


def reminder_in_group(request, id):
    filterByGroup = {'group_id': id}
    reminders_groups = ReminderGroup.objects.all().order_by('name')
    if (id != 'all'):
        reminders = Reminder.objects.filter(**filterByGroup).order_by('-name')
    else:
        reminders = Reminder.objects.all().order_by('-name')

    # paginator = Paginator(reminders_all, 128)
    # page = request.GET.get('page')
    # try:
    #     reminders = paginator.page(page)
    # except PageNotAnInteger:
    #     reminders = paginator.page(1)
    # except EmptyPage:
    #     reminders = paginator.page(paginator.num_pages)
    return render(request, 'app/reminder.html', { 'reminders' : reminders,
                                                  'reminders_groups': reminders_groups })


def reminder_in_time(request, time):
    # print("/reminder/time/: " + time)
    reminders_groups = ReminderGroup.objects.all().order_by('name')
    present_datetime = datetime.now()
    future_datetime = present_datetime
    if time == 'week':
        future_datetime = present_datetime + timedelta(days=7)
    elif time == 'month':
        future_datetime = present_datetime + monthdelta(1)
    elif time == 'year':
        future_datetime = present_datetime + monthdelta(12)
    reminders = Reminder.objects.filter(when__range=(present_datetime, future_datetime)).order_by('-name')
    # paginator = Paginator(reminders_all, 128)
    # page = request.GET.get('page')
    # try:
    #     reminders = paginator.page(page)
    # except PageNotAnInteger:
    #     reminders = paginator.page(1)
    # except EmptyPage:
    #     reminders = paginator.page(paginator.num_pages)
    return render(request, 'app/reminder.html', {'reminders': reminders,
                                                 'reminders_groups': reminders_groups})


def reminder_add(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            json_list = serialize('json', [Reminder.objects.get(id=post.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.reminder.insert_one(python_list[0])
            # print("/reminder/add: " + json_object + "; result: " + str(result.inserted_id))

            return redirect('reminder')
    else:
        form = ReminderForm()
    return render(request, 'app/reminder_form.html', {'form': form,
                                                 'title': 'New reminder',
                                                 'button': 'Add'})


def reminder_edit(request, id):
    reminder = get_object_or_404(Reminder, id=id)
    if request.method == "POST":
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            json_list = serialize('json', [Reminder.objects.get(id=post.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.reminder.replace_one({"pk": post.id}, python_list[0])
            # print("/reminder/edit: " + json_object + "; result: " + str(result.matched_count))

            return redirect('reminder')
    else:
        form = ReminderForm(instance=reminder)
    return render(request, 'app/reminder_form.html', {'form': form,
                                                 'title': 'Edit reminder',
                                                 'button': 'Save',
                                                 'id': reminder.id})


def reminder_remove(request, id):
    reminder = get_object_or_404(Reminder, id=id)
    Reminder.objects.get(id=id).delete()

    json_list = serialize('json', [reminder])
    python_list = json_util.loads(json_list)
    json_object = json_util.dumps(python_list[0])
    result = mongoDatabase.reminder.delete_one({"pk": int(id)})
    # print("/reminder/remove: " + json_object + "; result: " + str(result.deleted_count))

    return redirect('reminder')


def reminder_group_add(request):
    if request.method == "POST":
        form = ReminderGroupForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            json_list = serialize('json', [ReminderGroup.objects.get(id=post.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.reminder.insert_one(python_list[0])
            # print("/reminder/group/add: " + json_object + "; result: " + str(result.inserted_id))

            return redirect('reminder')
    else:
        form = ReminderGroupForm()
    return render(request, 'app/reminder_form.html', {'form': form,
                                                 'title': 'New group of reminders',
                                                 'button': 'Add'})


def reminder_group_edit(request, id):
    reminderGroup = get_object_or_404(ReminderGroup, id=id)
    if request.method == "POST":
        form = ReminderGroupForm(request.POST, instance=reminderGroup)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            json_list = serialize('json', [ReminderGroup.objects.get(id=post.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.reminder.replace_one({"pk": post.id}, python_list[0])
            # print("/reminder/edit: " + json_object + "; result: " + str(result.matched_count))

            return redirect('reminder')
    else:
        form = ReminderGroupForm(instance=reminderGroup)
    return render(request, 'app/reminder_form.html', {'form': form,
                                                      'title': 'Edit group of reminders',
                                                      'button': 'Save',
                                                      'id': reminderGroup.id})


def reminder_group_remove(request, id):
    reminderGroup = get_object_or_404(ReminderGroup, id=id)
    ReminderGroup.objects.get(id=id).delete()

    json_list = serialize('json', [reminderGroup])
    python_list = json_util.loads(json_list)
    json_object = json_util.dumps(python_list[0])
    result = mongoDatabase.reminder.delete_one({"pk": int(id)})
    # print("/reminder/remove: " + json_object + "; result: " + str(result.deleted_count))

    return redirect('reminder')


def reminder_add_to_calendar(request, id):
    # Get credential for Google API
    credential = api_google.api_google_credential()

    reminder = get_object_or_404(Reminder, id=id)

    service = build("calendar", "v3", credentials=credential)
    calendar = service.calendarList()
    calendarList = calendar.list(minAccessRole='owner').execute()
    for calendarItem in list(calendarList.get('items', [])):
        if calendarItem.get("summary") == reminder.group.name:
            # print("add \"" + reminder.name + "\" to calendar \"" + calendarItem.get("summary") + "\"")

            # Refer to the Python quickstart on how to setup the environment:
            # https://developers.google.com/calendar/quickstart/python
            # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
            # stored credentials.

            present_datetime = datetime.now(tz=reminder.when.tzinfo)
            reminder_datetime = reminder.when
            if present_datetime > reminder_datetime:
                while present_datetime > reminder_datetime:
                    if reminder.repeat == '1d':
                        reminder_datetime = reminder_datetime + timedelta(days=1)
                    elif reminder.repeat == '7d':
                        reminder_datetime = reminder_datetime + timedelta(days=7)
                    elif reminder.repeat == '14d':
                        reminder_datetime = reminder_datetime + timedelta(days=14)
                    elif reminder.repeat == '30d':
                        reminder_datetime = reminder_datetime + timedelta(days=30)
                    elif reminder.repeat == '1m':
                        reminder_datetime = reminder_datetime + monthdelta(1)
                    elif reminder.repeat == '2m':
                        reminder_datetime = reminder_datetime + monthdelta(2)
                    elif reminder.repeat == '3m':
                        reminder_datetime = reminder_datetime + monthdelta(3)
                    elif reminder.repeat == '1y':
                        reminder_datetime = reminder_datetime + monthdelta(12)
                    else:
                        break

            datetime_start = reminder_datetime
            datetime_end = datetime_start + timedelta(hours=1)

            # datetime.strptime(reminder.when, "%Y-%m-%d %H:%M:%S")
            # datetime_start.strftime("%Y-%m-%d %H:%M:%S"),

            event = {
                'summary': reminder.name,
                # 'location': '800 Howard St., San Francisco, CA 94103',
                # 'description': 'A chance to hear more about Google\'s developer products.',
                'start': {
                    'dateTime': datetime_start.isoformat("T"),
                    'timeZone': 'Europe/Warsaw',
                },
                'end': {
                    'dateTime': datetime_end.isoformat("T"),
                    'timeZone': 'Europe/Warsaw',
                },
                # 'recurrence': [
                #     'RRULE:FREQ=DAILY;COUNT=2'
                # ],
                # 'attendees': [
                #     {'email': 'lpage@example.com'},
                #     {'email': 'sbrin@example.com'},
                # ],
                # 'reminders': {
                #     'useDefault': False,
                #     'overrides': [
                #         {'method': 'email', 'minutes': 24 * 60},
                #         {'method': 'popup', 'minutes': 10},
                #     ],
                # },
            }

            event = service.events().insert(calendarId=calendarItem.get('id'), body=event).execute()
            # print('event created: %s' % (event.get('htmlLink')))

    return HttpResponseRedirect("/reminder")