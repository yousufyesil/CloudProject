import boto3

session = boto3.Session(
    aws_access_key_id='ASIA3DXXHYOMTINCIWWS',
    aws_secret_access_key='CJpxsKRL+69giTW3nwg3uA+3+WROPLjITGY2e7L3',
    aws_session_token='IQoJb3JpZ2luX2VjEO7//////////wEaCXVzLXdlc3QtMiJGMEQCIAuVIZ852Ffehld1oWPJgU4Xm8ifFOUI3PN4tngLdXveAiA0JVPCMEzyF9o6Ao3YdGqtqcM3q4cm3ZvivU+vpNiABCq6Agim//////////8BEAAaDDc2Mzk0ODk0MjIzMyIMRHK9ytbPWFarH55nKo4CRjriB6iLL+kUHwBxLt7qv7HW1IUJtfoXX3LDDuiMQgP4l8l9dIrqmNNGycghn9M0NqcA01kOrrSp6BO9g7kQh+fBHYHhb0BjWScf0EuS8cruAz95MRA+TzA7SOUChvHUMIJ2l6ANWsRrdKflgmO0W0xRU+ZzvLqLWUP4pUvvjUDmjlgLPQkFbsgDfheDaHRLQ5lJKUfXghQharivBor1OEXSfsSaGg5lAI3JXUx3asijGRmq5OyaUx2PR21RjkGXBS+l4ZFxsuTOLmXV1PDafxTpzsLsjN2dkmpMfG9vwDTmZeZ0dycp7tIeC2ifV4LcQoAMeA4rw/jeR+RFjxDrYFC/mp4Mb3RW4EHbPJCmMPOi5roGOp4B5kbrKXI6ZM5YoQYmj8fbvxFCXmS7rlLB3IDFBLxDwnB9BmMVTxniD3EKRQKl8XnyuIWzT/EnrndW2j66mhhgo3MVW61RfQs/l38pUWUpqCt37V0LKRJqn4NoCPKZOcYB7qCcruvk1bKzOxJMEfsx7c0XfR3Y/jVxwByhbt75697jsU7hILeZyctL4d7CjVttYWjdtNsYckwGcS6XFgU='
)

sqs_client = session.client('sqs', region_name='us-east-1')
sqs_client.send_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/790933937313/Xmas2024',
    MessageBody='Frohe Weihnachten',
    MessageAttributes ={
        'MatNr': {
            'DataType': 'String',
            'StringValue': '20237852'

        },
        'StudentName': {
            'DataType': 'String',
            'StringValue': 'Muhammad-Yousuf Yesil'

        },
        'Email-Adresse': {
            'DataType': 'String',
            'StringValue': 'yousufyesil@icloud.com'
        },
        'ReplyURL': {
            'DataType': 'String',
            'StringValue': 'https://sqs.us-east-1.amazonaws.com/763948942233/FDPQueue'
        },

    }
 )
print(sqs_client.receive_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/790933937313/Xmas2024'
))