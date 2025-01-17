#!/usr/bin/python3

import time
import os
import psycopg2
from boto3 import resource
from s3 import connect
import requests
from botocore.exceptions import ClientError

from bottle import route, run, template, request, app, Bottle, static_file

import boto3
connection = psycopg2.connect(
    user="postgres",
    host="awsbase.cw6qjfqpxzus.us-east-1.rds.amazonaws.com",
    password="postgres",
    database="bottletube"
)
connection.autocommit = True

cursor = connection.cursor()

# Schema auswählen
cursor.execute("SET SCHEMA 'bottletube';")
connection.commit()

@route('/hello')
@route('/healthcheck')
def healthcheck():
    return 'I feel lucky'

app = Bottle()
@app.route('/home')
@app.route('/')
def home():
    # Read Entries from DB
    # SQL Query goes here later, now dummy data only

    items = []
    cursor.execute("""SELECT * FROM image_uploads ORDER BY id""")

    for record in cursor.fetchall():
        items.append({
            'id': record[0],
            'filename': record[1],
            'category': record[2]
        })
    return template('home.tpl', name='BoTube Home', items=items)


@app.route('/upload', method='GET')
def do_upload_get():
    return template('upload.tpl', name='Upload Image')

@app.route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root='./static')  

@app.route('/upload', method='POST')
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
        if ext not in ('.png', '.jpg', '.jpeg'):
            error_messages.append('File Type not allowed.')
    except:
        error_messages.append('Unknown error.')

    if error_messages:
        return template('upload.tpl', name='Upload Image', error_messages=error_messages)

    # Save to /tmp folder
    upload.filename = name + '_' + time.strftime("%Y%m%d-%H%M%S") + ext
    upload.save('images')

    # Upload to S3
    data = open('images/' + upload.filename, 'rb')
    s3_resource.Bucket("yesil-20237852").put_object(Key='user_uploads/' + upload.filename,
                                                                             Body=data,
                                                                             ACL='public-read')

    # Write to DB
    cursor.execute(f"""
        INSERT INTO image_uploads (url, category)
        VALUES ('user_uploads/{save_filename}', '{category}');
    """)
    connection.commit()
    # some code has to go here later

    # Return template
    return template('upload_success.tpl', name='Upload Image')


if __name__ == '__main__':
    # Connect to DB
    # some code has to go here


    # Connect to S3
    connect()

    # Needs to be customized
    # run(host='your_public_dns_name',
    run(app, host='localhost', port=8080, debug=True)

