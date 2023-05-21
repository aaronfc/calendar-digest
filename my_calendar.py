from icalendar import Calendar, Event
import recurring_ical_events
import requests
import datetime
import pytz

def get_events(ics_url, days):
    # Reading calendar and extracting events
    gcal = Calendar.from_ical(requests.get(ics_url).text)

    present = datetime.date.today()
    localtz = pytz.timezone('Europe/Madrid')
    d = datetime.timedelta(days)

    # Using `recurring_ical_events` so that recurring events are correctly parsed.
    events = []
    for component in recurring_ical_events.of(gcal, keep_recurrence_attributes=True).between(present, present + d):
        if component.name == "VEVENT":
            dtstart = component.get('dtstart').dt
            dtend = None
            dttimestart = None
            dttimeend = None
            if 'dtend' in component:
                dtend = component.get('dtend').dt

            if isinstance(dtstart, datetime.datetime):
                dttimestart = dtstart.astimezone(localtz)
                dtstart = dttimestart.date()
            if isinstance(dtend, datetime.datetime):
                dttimeend = dtend.astimezone(localtz)
                dtend = dttimeend.date()

            if dtend != None and dtend >= present:
                if dtstart >= present and dtstart <= present + d:
                    # Skip some recurrent events
                    if 'rrule' in component:
                        frequency = component.get('rrule').get('freq')
                        # Skip daily events - we are not interested in them.
                        if 'DAILY' in frequency:
                            continue
                        # Skip weekly events (and only _purely_ weekly events)
                        if 'WEEKLY' in frequency:
                            # But not if they are not really weekly (bi-weekly or so)
                            if 'interval' not in component.get('rrule'):
                                continue
                    events.append({
                        "summary": component.get('summary'),
                        "start_date": dtstart,
                        "end_date": dtend,
                        "start_datetime": dttimestart,
                        "end_datetime": dttimeend,
                        "location": component.get('location')
                    })
    events_per_day = {}
    for event in events:
        date = event['start_date']
        if date not in events_per_day:
            events_per_day[date] = []
        events_per_day[date].append(event)
    return events_per_day

if __name__ == "__main__":
    from config import CALENDAR_ICS_URL, DAYS
    from pprint import pprint
    pprint(get_events(CALENDAR_ICS_URL, DAYS))
