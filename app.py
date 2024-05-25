import logging
from flask import Flask
import psycopg2
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Ensure the environment variable for Key Vault name is set
keyVaultName = os.environ.get("KEYVAULTNAME")
if not keyVaultName:
    logging.error("KEYVAULTNAME environment variable not set")
    raise Exception("KEYVAULTNAME environment variable not set")

KVUri = f"https://{keyVaultName}.vault.azure.net"
logging.info(f"Key Vault URI: {KVUri}")

# Initialize the Azure Key Vault client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

try:
    # Fetch the database credentials from Azure Key Vault
    db_name = client.get_secret("DBNAME").value
    db_user = client.get_secret("DBUSER").value
    db_password = client.get_secret("DBPASSWORD").value
    db_host = client.get_secret("DBHOST").value
    logging.info("Successfully retrieved secrets from Key Vault")
except Exception as e:
    logging.error(f"Failed to retrieve secrets from Key Vault: {e}")
    raise

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
        logging.info("Database connection successful")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

@app.route('/hello')
def hello():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        conn.close()
        return "Hello, World! DB Connection Successful by Konege" if result else "DB Connection Failed"
    except Exception as e:
        logging.error(f"Error in /hello route: {e}")
        return f"DB Connection Failed: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
