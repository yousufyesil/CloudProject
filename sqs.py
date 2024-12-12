import boto3

session = boto3.Session(
    aws_access_key_id='ASIA3DXXHYOMY2RM5ZTV',
    aws_secret_access_key='W2SEQb1VV1GzZeco6ujw1ME1Eu5Bd2qo+TlHRnbJ',
    aws_session_token='IQoJb3JpZ2luX2VjEAAaCXVzLXdlc3QtMiJHMEUCIEhvHc46p26KsE8rq+DxefN+rZd4rv1HJazH49NpwBLGAiEAwjlJo2DYZt4JnYN4p0cxm4g3GcIbprhc0AVeJy66oXMqugIIuf//////////ARAAGgw3NjM5NDg5NDIyMzMiDI4WUlCefhWfpzg0PCqOAsmLS1N8sXIcZo+en8mRIB7DkKxtRDqzUKde6GfWhk4CVQHSoe7mo+zmAIIi8s4S+GZ0lZz2BqEJAnFKoiWFOGKPTSLarlvL+o926U5bPV/cDJbBReVS3A/UVZ7U+c9xM2D+I0T3WMFa4wKCouiq4ElMbBu6IZOzncTtPlKtq+66AEpf3G50sL+Ed8MNZeukQcDEyjVPGaLjSA4ckQzC6DZUryK/G5nav8KUhg1S+cWtAR6yRe+4ET8n5i9U/7Chv3t6eDI0en7kACF14E+raz6HXBEE3xdCLNr4E1HDjHY8oDA60nMWMgz5IQMDyQ5AYxP5tYjL7+tCwqdLxA2HoK8x5BxIz5qzebKH+jBdYjCfo+q6BjqdAeQiXu7Ak3YkwYwE1OZStlI9pTwAlJzVt9PCaIE+clitYKPf5qrRIESzdvEJ97QKOjH5zNDpWiNF7UMrQenfEPj2gRxhN71WM5jCiCiFRhTSimcMI7BnMqTdeb27MN+p7k+LVN7GAD2ti86QsoXlZEeRDPx28HmxJugJaubKmG8vQFnk28HDEsLtAClTHtaZPUPOvFbJbdPE+fSTpWs='
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
