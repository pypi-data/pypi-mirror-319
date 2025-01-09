import requests

def list_surveys(token):
    url = "https://api.inovyo.com/v2/survey/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Falha ao listar pesquisas: {response.status_code} - {response.text}")

def get_survey_responses(token, survey_id, start_date=None, end_date=None, limit=100, page=1, order="asc"):
    url = f"https://api.inovyo.com/v2/survey/{survey_id}/responses"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "page": page,
        "order": order
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Falha ao obter respostas da pesquisa: {response.status_code} - {response.text}")

def get_survey_questions(token, survey_id):
    url = f"https://api.inovyo.com/v2/survey/{survey_id}/questions"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Falha ao obter questões da pesquisa: {response.status_code} - {response.text}")
