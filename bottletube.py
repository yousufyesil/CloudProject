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
    public_dns = requests.get('http://169.254.169.254/latest/meta-data/public-hostname').text
    return f'I feel lucky @ {public_dns}'

@route('/bonusql')
def bonusql():
    return template('bonusql.tpl', name='Bonusql')

@route('/delete')
@route('/delete/<id:int>')


@route('/delete/<id:int>')
def delete(id):
    try:
        cursor.execute("SELECT url FROM image_uploads WHERE id = %s", (id,))
        result = cursor.fetchone()
        if result:
            file_url = result[0]
            s3_resource.Object("yesil-20237852", file_url).delete()
            cursor.execute("DELETE FROM image_uploads WHERE id = %s", (id,))
            connection.commit()

        from bottle import redirect
        return redirect('/')

    except Exception as e:
        print(f"Error deleting image: {str(e)}")
        from bottle import redirect
        return redirect('/')
    except Exception as e:
        print(f"Error deleting image: {str(e)}")
        # Auch im Fehlerfall die aktuelle Liste anzeigen
        items = []
        cursor.execute("""SELECT * FROM image_uploads ORDER BY id""")
        for record in cursor.fetchall():
            items.append({
                'id': record[0],
                'filename': record[1],
                'category': record[2]
            })
        return template('home.tpl', name='BoTube Home', items=items)
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
    # SQL Query goes here later, now dummy data only

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
        if ext not in ('.png', '.jpg', '.jpeg','.webp','.pdf'):
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
    cursor.execute(f"INSERT INTO image_uploads (url, category) VALUES ('user_uploads/{upload.filename}', '{category}');")
    connection.commit()
    # some code has to go here later

    # Return template
    return template('upload_success.tpl', name='Upload Image')


if __name__ == '__main__':
    run(host=requests.get('http://169.254.169.254/latest/meta-data/public-hostname').text,
        port=80)

if True:  # wird immer ausgeführt
    import os
    from bottle import default_app

    # Datenbank- und AWS-Konfiguration
    sm_session = session.Session()
    client = sm_session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    secret = json.loads(
        client.get_secret_value(SecretId='ddaypaper')
        .get('SecretString')
    )

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

    # S3 Verbindung
    s3_resource = resource('s3', region_name='us-east-1')

    os.chdir(os.path.dirname(__file__))
    application = default_app()