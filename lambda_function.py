from icalendar import Calendar, Event
import requests
import datetime
import pytz
import json
import boto3
from botocore.exceptions import ClientError
from config import CALENDAR_ICS_URL, RECIPIENT, SENDER, DAYS

# Testing
SEND_EMAIL = True

# Reading calendar and extracting events
gcal = Calendar.from_ical(requests.get(CALENDAR_ICS_URL).text)

present = datetime.date.today()
localtz = pytz.timezone('Europe/Madrid')

d = datetime.timedelta(DAYS)

events = []
for component in gcal.walk():
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

# Generating email body
body = """<html>
<head></head>
<body>
  <h1>Your next week!</h1>
  """
for day in sorted(events_per_day):
    body += "<h2>" + str(day) + "</h2>\n"
    for event in sorted(events_per_day[day], key=lambda e: e['start_datetime'] if e['start_datetime'] != None else datetime.datetime.now(localtz)):
        body += "<p> * {}: {}</p>\n".format(event['start_datetime'].strftime("%H:%M") if event['start_datetime'] != None else "all day", event['summary'])

body += """
</body>
</html>"""            

def send_email(sender, recipient, body):
    AWS_REGION = "eu-west-3"
    SUBJECT = "Your next week!"
    CHARSET = "UTF-8"

    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=sender,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def lambda_handler(event, context):
    # Main program
    send_email(SENDER, RECIPIENT, body)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    if SEND_EMAIL:
        send_email(SENDER, RECIPIENT, body)
    else:
        print(body)
