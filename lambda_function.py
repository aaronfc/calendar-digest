import requests
import json
import boto3
from botocore.exceptions import ClientError
from config import CALENDAR_ICS_URL, RECIPIENT, SENDER, DAYS
from acalendar import email, template, calendar

def lambda_handler(event, context):
    # Main program
    events_per_day = calendar.get_events(CALENDAR_ICS_URL, DAYS)
    body = template.generate(events_per_day)
    email.send_email(SENDER, RECIPIENT, body)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    lambda_handler({}, {})
