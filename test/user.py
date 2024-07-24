import requests

SERVER_URL = 'http://0.0.0.0:3000'

def login_process():
    try:
        result = requests.post(SERVER_URL+'/user', json={'user_name':'John Doe','password':'1234'})
        print(result.text)
    except:
        pass # do nothing, user exists
    result = requests.post(SERVER_URL+'/token', json={'user_name':'John Doe','password':'1234'})
    print(result.text)
    token = result.json()['access_token']
    return token

def use_token(token: str):
    # Test with valid token
    result = requests.get(SERVER_URL+"/secure-endpoint", headers={"Authorization": f"Bearer {token}"})
    assert(result.status_code == 200) 
    
    # Test with invalid token
    result = requests.get(SERVER_URL+"/secure-endpoint", headers={"Authorization": f"Bearer ABC.123"})
    assert(res)
    
    # Test with no token
    result = requests.get(SERVER_URL+"/secure-endpoint")
    print(result.text)
    
if __name__ == "__main__":
    token = login_process()
    use_token(token)
