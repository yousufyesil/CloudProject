#!/usr/bin/python3

import time
import os
import psycopg2
import requests
import json
from bottle import route, run, template, request, app, static_file
from boto3 import resource, session

# Healthcheck-Route - einfacher Test, ob der Service läuft
@route('/hello')
@route('/healthcheck')
def healthcheck():
    # Verwenden der EC2-Metadaten für einen aussagekräftigeren Healthcheck
    return requests.get('http://169.254.169.254/latest/meta-data/public-hostname').text

@route('/home')
@route('/')
def home():
    # Lese alle Einträge aus der Datenbank
    items = []
    cursor.execute("""SELECT * FROM image_uploads ORDER BY id""")

    for record in cursor.fetchall():
        items.append({
            'id': record[0],
            'filename': record[1],
            'category': record[2]
        })

    return template('home.tpl', name='BoTube Home', items=items)

# Statische Dateien bereitstellen
@route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root='./static')

# Upload-Formular anzeigen
@route('/upload', method='GET')
def do_upload_get():
    return template('upload.tpl', name='Upload Image')

# Datei-Upload verarbeiten
@route('/upload', method='POST')
def do_upload_post():
    category = request.forms.get('category')
    upload = request.files.get('file_upload')

    # Fehlerprüfung
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

    # Datei temporär speichern
    upload.filename = name + '_' + time.strftime("%Y%m%d-%H%M%S") + ext
    upload.save('images')

    # Zu S3 hochladen
    data = open('images/' + upload.filename, 'rb')
    s3_resource.Bucket("yesil-20237852").put_object(
        Key='user_uploads/' + upload.filename,
        Body=data,
        ACL='public-read'
    )

    # In Datenbank speichern
    cursor.execute(
        f"INSERT INTO image_uploads (url, category) VALUES ('user_uploads/{upload.filename}', '{category}');"
    )
    connection.commit()

    # Erfolgsseite anzeigen
    return template('upload_success.tpl', name='Upload Image')

if __name__ == '__main__':
    # Verbindung zum AWS Secrets Manager herstellen
    sm_session = session.Session()
    client = sm_session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    # Datenbank-Zugangsdaten aus Secrets Manager abrufen
    secret = json.loads(
        client.get_secret_value(SecretId='ddaypaper')
        .get('SecretString')
    )

    # Datenbankverbindung aufbauen
    connection = psycopg2.connect(
        user=secret['username'],
        host=secret['host'],
        password=secret['password'],
        database=secret['dbname']
    )
    connection.autocommit = True
    cursor = connection.cursor()

    # Schema setzen
    cursor.execute("SET SCHEMA 'bottletube';")
    connection.commit()
#d
    # S3-Verbindung aufbauen
    s3_resource = resource('s3', region_name='us-east-1')

    # Server starten
    run(host='ec2-54-91-156-193.compute-1.amazonaws.com',
        port=80)