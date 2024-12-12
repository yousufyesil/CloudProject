#!/usr/bin/python3

# Standard-Bibliotheken importieren
import time
import os
import sys
import json

# Web- und Datenbank-Bibliotheken
import psycopg2
import requests
from bottle import route, run, template, request, app, static_file, default_app
from botocore.exceptions import ClientError

# AWS-spezifische Imports
from boto3 import resource, session
import boto3


# Route für Healthcheck
@route('/hello')
@route('/healthcheck')
def healthcheck():
    # Gibt den EC2 Hostnamen zurück für besseres Monitoring
    return requests.get('http://169.254.169.254/latest/meta-data/public-hostname').text


# Hauptseite mit Bildergalerie
@route('/home')
@route('/')
def home():
    # Alle Einträge aus der Datenbank lesen
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


# Upload-Logik
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

    # Datei speichern mit Zeitstempel
    upload.filename = name + '_' + time.strftime("%Y%m%d-%H%M%S") + ext
    save_path = os.path.join(os.path.dirname(__file__), 'images')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    upload.save(save_path)

    # Zu S3 hochladen
    try:
        data = open(os.path.join(save_path, upload.filename), 'rb')
        s3_resource.Bucket("yesil-20237852").put_object(
            Key='user_uploads/' + upload.filename,
            Body=data,
            ACL='public-read'
        )
    finally:
        data.close()

    # Datenbank-Eintrag erstellen
    cursor.execute(
        "INSERT INTO image_uploads (url, category) VALUES (%s, %s);",
        (f'user_uploads/{upload.filename}', category)
    )
    connection.commit()

    return template('upload_success.tpl', name='Upload Image')


# Hauptausführungsblock
if __name__ == '__main__':
    # Dieser Teil wird nur beim direkten Ausführen verwendet (Entwicklung)
    try:
        # AWS Secrets Manager Setup
        sm_session = session.Session()
        client = sm_session.client(
            service_name='secretsmanager',
            region_name='us-east-1'
        )

        # Datenbank-Zugangsdaten aus Secrets Manager holen
        secret = json.loads(
            client.get_secret_value(SecretId='PostgresBottle')
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

        # S3 Verbindung aufbauen
        s3_resource = resource('s3', region_name='us-east-1')

        # Entwicklungsserver starten
        host = requests.get('http://169.254.169.254/latest/meta-data/public-hostname').text
        run(host=host, port=80)
    except Exception as e:
        print(f"Startup error: {e}", file=sys.stderr)
        sys.exit(1)

# WSGI Anwendung konfigurieren
else:
    # Dieser Teil wird von Apache/WSGI verwendet
    try:
        # Gleiche Initialisierung wie oben
        sm_session = session.Session()
        client = sm_session.client(
            service_name='secretsmanager',
            region_name='us-east-1'
        )

        secret = json.loads(
            client.get_secret_value(SecretId='PostgresBottle')
            .get('SecretString')
        )

        connection = psycopg2.connect(
            user=secret['username'],
            host=secret['host'],
            password=secret['password'],
            database=secret['dbname']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("SET SCHEMA 'bottletube';")
        connection.commit()

        s3_resource = resource('s3', region_name='us-east-1')

        # Arbeitsverzeichnis setzen
        os.chdir(os.path.dirname(__file__))

        # WSGI-Anwendung erstellen
        application = default_app()
    except Exception as e:
        print(f"WSGI startup error: {e}", file=sys.stderr)
        sys.exit(1)