import requests
class WebUser:
    def __init__(user_name: str, password: str):
        pass
    def sign_in(user_name: str, password: str):
        pass
    def log_in(user_name: str, password: str):
        pass
    requests.post(
            '/user',
            json={
                'user_name': '1 @#rTHFGJ',
                'password': 'password1234'}
        )
        assert responce.status_code == 409 # Failed to create user: reason
