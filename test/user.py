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

if __name__ == "__main__":
    login_process()
