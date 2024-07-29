import requests

SERVER_URL = 'http://0.0.0.0:3000'

def login_process():
    try:
        result = requests.post(SERVER_URL+'/user', json={'user_name':'John Doe','password':'1234'}, timeout=1)
        print(result.text)
    except Exception:
        pass # do nothing, user exists
    result = requests.post(SERVER_URL+'/token', json={'user_name':'John Doe','password':'1234'}, timeout=1)
    print(result.text)
    token = result.json()['access_token']
    return token

def use_token(token: str):
    # Test with valid token
    result = requests.get(
        SERVER_URL+"/secure-endpoint",
        headers={"Authorization": f"Bearer {token}"},
        timeout=1
    )
    # Expecting 200 - OK
    assert result.status_code == 200

    # Test with invalid token
    result = requests.get(
        SERVER_URL+"/secure-endpoint",
        headers={"Authorization": "Bearer ABC.123"},
        timeout=1
    )
    # Expecting 403 - Forbidden
    assert result.status_code == 403

    # Test with no token, no credentials
    result = requests.get(SERVER_URL+"/secure-endpoint", timeout = 1)
    # Expecting 401 - Unauthorized
    assert result.status_code == 401

    # Test with no token, with credentials
    #result = requests.get(SERVER_URL+"/secure-endpoint", json={'user_name':'John Doe','password':'1234'}, timeout = 1)
    # Expecting 200 - OK
    #assert(result.status_code == 200)

def run_project():
    # Create user
    requests.post(
        SERVER_URL+"/user",
        json={'user_name': 'John Doe', 'password': '1234'},
        timeout=1
    )
    # Get user token
    token = requests.post(SERVER_URL+'/token', json={'user_name':'John Doe','password':'1234'}, timeout=1)
    token = token.json()['access_token']

    # Read project
    responce = requests.get(
        SERVER_URL+"/project/myproject",
        headers={"Authorization": f"Bearer {token}"},
        timeout=1
    )
    
    # Delete project
    responce = requests.delete(
        SERVER_URL+"/project/myproject",
        headers={"Authorization": f"Bearer {token}"},
        timeout=1
    )
    # Create project
    responce = requests.post(
        SERVER_URL+"/project/myproject",
        headers={"Authorization": f"Bearer {token}"},
        timeout=1
    )
    project_id = responce.json()['project_id']
    
    # Run project
    responce = requests.post(
        SERVER_URL+"/run/"+project_id,
        headers={"Authorization": f"Bearer {token}"},
        timeout=1
    )
    result_id = responce.text
    responce = requests.post(
        SERVER_URL+"/result",
        json={'result_id': result_id},
        headers={"Authorization": f"Bearer {token}"},
        timeout=1
    )

if __name__ == "__main__":
    token = login_process()
    use_token(token)
    run_project()
