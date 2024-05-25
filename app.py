from flask import Flask
import psycopg2
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

app = Flask(__name__)

# Ensure the environment variable for Key Vault name is set
keyVaultName = os.environ.get("KEY_VAULT_NAME")
if not keyVaultName:
    raise Exception("KEY_VAULT_NAME environment variable not set")

KVUri = f"https://{keyVaultName}.vault.azure.net"

# Initialize the Azure Key Vault client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

# Fetch the database credentials from Azure Key Vault
db_name = client.get_secret("DBNAME").value
db_user = client.get_secret("DBUSER").value
db_password = client.get_secret("DBPASSWORD").value
db_host = client.get_secret("DBHOST").value

def get_db_connection():
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )
    return conn

@app.route('/hello')
def hello():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    result = cursor.fetchone()
    conn.close()
    return "Hello, World! DB Connection Successful by Konege" if result else "DB Connection Failed"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
