from boto3 import resource

def connect():
    s3 = resource('s3', region_name='us-east-1')
    s3.Object('yesil-20237852', 'hello.py').put(Body=open('footer.tpl', 'rb'))

