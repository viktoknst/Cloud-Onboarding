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
    try:
        result = requests.get(SERVER_URL+"/secure-endpoint", headers={"Authorization": f"Bearer {token}"})
        print(result.text)
    except:
        print(result.text)
        pass # do nothing, user exists
    try:
        result = requests.get(SERVER_URL+"/secure-endpoint", headers={"Authorization": f"Bearer Hi.there"})
        print(result.text)
    except:
        print(result.text)
        pass # do nothing, user exists
    try:
        result = requests.get(SERVER_URL+"/secure-endpoint")
        print(result.)
    except:
        print(result)
        pass # do nothing, user exists

if __name__ == "__main__":
    token = login_process()
    use_token(token)
