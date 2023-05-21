import boto3
from botocore.exceptions import ClientError

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

if __name__ == "__main__":
    send_email('sender@email.com', 'receiver@email.com', '<strong>HTML Body</strong>')
