import psycopg2

# Verbindung zur Datenbank herstellen
connection = psycopg2.connect(
    user="postgres",
    host="awsbase.cw6qjfqpxzus.us-east-1.rds.amazonaws.com",
    password="postgres",
    database="bottletube"
)
cursor = connection.cursor()

# Schema auswählen
cursor.execute("SET SCHEMA 'bottletube';")
connection.commit()