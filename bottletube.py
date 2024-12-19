#!/usr/bin/python3

import time
import os
import sys
import psycopg2
import requests
from botocore.exceptions import ClientError
import json
from bottle import route, run, template, request, app, static_file, default_app
from boto3 import resource, session
import boto3


@route('/hello')
@route('/healthcheck')
def healthcheck():
    return 'I feel lucky'


@route('/bonusql')
def bonusql():
    return template('bonusql.tpl', name='Bonusql')


@route('/home')
@route('/')
def home():
    # Read Entries from DB
    items = []
    cursor.execute("""SELECT * FROM image_uploads ORDER BY id""")

    for record in cursor.fetchall():
        items.append({
            'id': record[0],
            'filename': record[1],
            'category': record[2]
        })

    return template('home.tpl', name='BoTube Home', items=items)


@route('/upload', method='GET')
def do_upload_get():
    return template('upload.tpl', name='Upload Image')


@route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root='./static')


@route('/upload', method='POST')
def do_upload_post():
    category = request.forms.get('category')
    upload = request.files.get('file_upload')

    # Check for errors
    error_messages = []
    if not upload:
        error_messages.append('Please upload a file.')
    if not category:
        error_messages.append('Please enter a category.')

    try:
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.png', '.jpg', '.jpeg', '.webp', '.pdf'):
            error_messages.append('File Type not allowed.')
    except:
        error_messages.append('Unknown error.')

    if error_messages:
        return template('upload.tpl', name='Upload Image', error_messages=error_messages)

    # Save to images folder
    upload.filename = name + '_' + time.strftime("%Y%m%d-%H%M%S") + ext
    upload.save('images')

    # Upload to S3
    data = open('images/' + upload.filename, 'rb')
    s3_resource.Bucket("yesil-20237852").put_object(Key='user_uploads/' + upload.filename,
                                                    Body=data,
                                                    ACL='public-read')

    # Write to DB
    cursor.execute(
        f"INSERT INTO image_uploads (url, category) VALUES ('user_uploads/{upload.filename}', '{category}');")
    connection.commit()

    return template('upload_success.tpl', name='Upload Image')


# Database and AWS connection setup
def setup_connections():
    global connection, cursor, s3_resource

    # AWS Secrets Manager Setup
    sm_session = session.Session()
    client = sm_session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    # Get secrets from AWS Secrets Manager
    secret = json.loads(
        client.get_secret_value(SecretId='ddaypaper')
        .get('SecretString')
    )

    # Database connection
    connection = psycopg2.connect(
        user=secret['username'],
        host=secret['host'],
        password=secret['password'],
        database=secret['dbInstanceIdentifier']
    )
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute("SET SCHEMA 'bottletube';")
    connection.commit()

    # S3 connection
    s3_resource = resource('s3', region_name='us-east-1')


# Initialize connections
setup_connections()

if __name__ == '__main__':
    # Development server
    run(host='ec2-34-204-125-209.compute-1.amazonaws.com',
        port=5050)
else:
    # Production WSGI server
    os.chdir(os.path.dirname(__file__))
    application = default_app()