from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils import dateparse
from googleapiclient.discovery import build

from . import api_google

def calendar(request):
    # Get credential for Google API
    credential = api_google.api_google_credential()

    # Build a service object for the API that you want to call
    service = build("calendar", "v3", credentials=credential)

    # Make requests to the API service using the interface provided by the service object.
    # Get collection of calendars in the user's calendar list
    calendar = service.calendarList()

    # Use calendarList, which method list() returns entries on the user's calendar list
    calendarList = calendar.list(minAccessRole='owner').execute()
    # utils.console("List of calendars from Google API:")
    # utils.object2json(calendarList)

    # Prepare list for events
    eventsList = []
    calendarEvents = []

    # Prepare filter while getting events from calendars
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    year = (datetime.utcnow() + timedelta(days=365)).isoformat() + 'Z'  # 'Z' indicates UTC time

    # For each calendar get events using prepared filters
    for calendarItem in list(calendarList.get('items', [])):
        result = service.events().list(
            calendarId=calendarItem.get('id'),
            maxResults=250,
            singleEvents=True,
            timeMin=now,
            timeMax=year,
            orderBy='startTime').execute()
        events = result.get('items', [])

        # Store events in list with all events from all calendars
        eventsList.extend(events)

        # Prepare dedicated list with selected attributes from calendar and events
        for event in events:
            calendarEvent = {}
            calendarEvent["calendar"] = calendarItem.get("summary")
            calendarEvent["color"] = calendarItem.get("backgroundColor")
            calendarEvent["date"] = event.get("start").get("date") if event.get("start").get("date") else dateparse.parse_datetime(event.get("start").get("dateTime")).date().isoformat()
            calendarEvent["time"] = dateparse.parse_datetime(event.get("start").get("dateTime")).time().isoformat() if event.get("start").get("dateTime") else "- - -"
            calendarEvent["event"] = event.get("summary")
            calendarEvents.append(calendarEvent)

    # Sort dedicated list by date
    sortedCalendarEvents = sorted(calendarEvents, key=lambda k: k['date'])

    # utils.console("List of events from Google API:")
    # utils.object2json(eventsList)

    # utils.console("List of calendar events created from calendar and events:")
    # utils.object2json(calendarEvents)

    # Render view with the list of calendars
    return render(request, 'app/calendar.html', {
        'calendarList': calendarList,
        'eventsList': eventsList,
        'calendarEvents': sortedCalendarEvents
    })