import requests

def generate_token(api_token, api_secret):
    url = "https://api.inovyo.com/v2/auth"
    payload = {
        "expire": 60,
        "api_token": api_token,
        "api_secret": api_secret
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get('token')
    else:
        raise Exception(f"Falha na autenticação: {response.status_code} - {response.text}")

def verify_token(token):
    url = "https://api.inovyo.com/v2/verify_token"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Falha na verificação do token: {response.status_code} - {response.text}")
