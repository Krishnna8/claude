# app.py
from flask import Flask
import hvac
import os

app = Flask(__name__)

def get_vault_secret():
    vault_client = hvac.Client(
        url='http://vault.vault.svc.cluster.local:8200',
        token=os.getenv('VAULT_TOKEN')
    )
    
    try:
        secret = vault_client.read('secret/data/app-config')
        return secret['data']['data']['message'] if secret else 'No message found'
    except Exception as e:
        return f'Error reading from vault: {str(e)}'

@app.route('/')
def hello():
    message = get_vault_secret()
    return f'Message from Vault: {message}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
