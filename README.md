# ACalendar
Quick PoC to send a weekly preview of the calendar for the next upcoming weeks.

## Notes
- Using public(but private) `*.ics` url from Google Calendar's Aaron calendar.
- Using `icalendar` python package to handle the `*.ics` format.
- Getting events in the next 14 days and group by day. Some events have time and others don't (are all-day events)
- Sending email using Simple Email Service from AWS.
	- We are currently relying on the `Alexa` identity I had in my local machine.
	- I had to add Access to SES service to the `Alexa` identity. `AmazonSESReadOnlyAccess` and `AmazonSESFullAccess`
	- SES account is sandboxed so we can only send from and **to** verified email addresses (enough!)
- Script is running correctly.
- Making it run every Sunday at 8AM with an AWS Lambda function.
	- Renamed the `main.py` to `lambda_function.py` and added some handler inside.
	- Had to run some building process to properly add dependencies in the lambda code. See `build.sh`.
	- Had to add again permissions to SES service to the Lambda instance Role (see IAM console)
	- Clicking `Test` button in the lambda ui sent the email successfully.
	- In the Lambda UI by clicking the Trigger button and configuring a trigger based on "EventBridge (old CloudWatch events)" with the following cron: `cron(00 06 ? * SUN *)`.

- Next:
	- Cleanup code
	- Template engine or better html generation
	- See if we can use `Zappa` which apparently might reduce complexity on deploy/building et all.
	- Write blog post?

## References
- Sending emails: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
