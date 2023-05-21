import datetime
import pytz

def generate(events_per_day):
    localtz = pytz.timezone('Europe/Madrid')
    
    body = """<html>
    <head></head>
    <body>
    <h1>Get ready for upcoming events!🚀</h1>
"""
    for day in sorted(events_per_day):
        tag = "h2" if day - datetime.datetime.today().date() <= datetime.timedelta(days=7) else "h3"
        body += "    <" + tag + ">" + day.strftime("%d/%m/%Y %A") + "</" + tag + ">\n"
        for event in sorted(events_per_day[day], key=lambda e: e['start_datetime'] if e['start_datetime'] != None else datetime.datetime.now(localtz) - datetime.timedelta(days = 1)):
            body += "    <p> * {}: {}</p>\n".format(event['start_datetime'].strftime("%H:%M") if event['start_datetime'] != None else "all day", event['summary'])

    body += """
    </body>
    </html>"""
    return body

if __name__ == "__main__":
    localtz = pytz.timezone('Europe/Madrid')
    now = datetime.datetime.now(localtz)
    print(generate({
        now.date(): [{'start_datetime': now + datetime.timedelta(seconds=300), 'summary': 'And also later'}, {'start_datetime': now, 'summary': 'During morning'}, {'start_datetime': None, 'summary': 'Testing all day'}],
        now.date() + datetime.timedelta(days=9): [{'start_datetime': now+datetime.timedelta(days=9), 'summary': 'This is the following week'}],
    }))
