import requests

class WebClient:
    def __init__(self, user_name: str, password: str, server_url: str):
        self.user_name = user_name
        self.password = password
        self.server_url = server_url
        self.auth_header = None


    def sign_in(self):
        responce = requests.post(
            self.server_url + '/user',
            json =
            {
                'user_name': self.user_name,
                'password': self.password
            }
        )

        return responce
    

    def log_in(self):
        responce = requests.post(
            self.server_url + '/token',
            json = 
            {
                'user_name': self.user_name,
                'password': self.password
            }
        )

        if responce.status_code != 200:
            return responce

        token = responce.json()['access_token']
        self.auth_header = {"Authorization": f"Bearer {token}"}
        return responce


    def rename(self, new_name: str):
        if not self.auth_header:
            return
        
        responce = requests.put(
            self.server_url + '/user',
            json =
            {
                'user_name': new_name,
                'password': self.password
            },
            headers = self.auth_header
        )

        if self.log_in().status_code == 200:
            self.user_name = new_name

        return responce


    def delete(self):
        responce = requests.delete(
            self.server_url + '/user',
            headers = self.auth_header
        )

        return responce


    def change_password(self, new_password):
        if not self.auth_header:
            return
        
        responce = requests.put(
            self.server_url + '/user',
            json =
            {
                'user_name': self.user_name,
                'password': new_password
            },
            headers = self.auth_header
        )

        if self.log_in().status_code == 200:
            self.password = new_password

        return responce
    

    def create_project(self, project_name):
        if not self.auth_header:
            return

        responce = requests.post(
            self.server_url + f'/project/{project_name}',
            headers = self.auth_header
        )

        return responce
    
