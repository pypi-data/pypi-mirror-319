import requests

def list_contacts(token):
    url = "https://api.inovyo.com/v2/contact/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Falha ao listar contatos: {response.status_code} - {response.text}")

def get_contact_details(token, contact_id):
    url = f"https://api.inovyo.com/v2/contact/{contact_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Falha ao obter detalhes do contato: {response.status_code} - {response.text}")

def get_contact_survey_link(token, contact_id):
    url = f"https://api.inovyo.com/v2/contact/survey_link"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"contact_id": contact_id}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Falha ao obter link da pesquisa para o contato: {response.status_code} - {response.text}")

def send_batch_contacts(token, contacts_data):
    url = "https://api.inovyo.com/v2/contact/batch"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(url, headers=headers, json=contacts_data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Falha ao enviar dados em lote para contatos: {response.status_code} - {response.text}")

def set_contact_webhook(token, webhook_url):
    url = "https://api.inovyo.com/v2/contact/webhook"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"webhook_url": webhook_url}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Falha ao configurar webhook de contatos: {response.status_code} - {response.text}")
