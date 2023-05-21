import requests
import json
import boto3
from botocore.exceptions import ClientError
from config import CALENDAR_ICS_URL, RECIPIENT, SENDER, DAYS
import my_email
import my_template
import my_calendar

def lambda_handler(event, context):
    # Main program
    events_per_day = my_calendar.get_events(CALENDAR_ICS_URL, DAYS)
    body = my_template.generate(events_per_day)
    my_email.send_email(SENDER, RECIPIENT, body)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    lambda_handler({}, {})
