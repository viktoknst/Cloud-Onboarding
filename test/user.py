from context import *

@mock.patch('os.mkdir', new=does_nothing)
@mock.patch('os.path.exists', new=always_false)
class TestExampleUser:

    def test_login_process(self):
    
        result = client.post('/user', json={'user_name':'John Doe','password':'1234'}, timeout=1)
        print(result.text)
        result = client.post('/token', json={'user_name':'John Doe','password':'1234'}, timeout=1)
        print(result.text)
        token = result.json()['access_token']
        return token

    def use_token(self, token: str):
        # Test with valid token
        result = client.get(
            "/secure-endpoint",
            headers={"Authorization": f"Bearer {token}"},
            timeout=1
        )
        # Expecting 200 - OK
        assert result.status_code == 200

        # Test with invalid token
        result = client.get(
            "/secure-endpoint",
            headers={"Authorization": "Bearer ABC.123"},
            timeout=1
        )
        # Expecting 403 - Forbidden
        assert result.status_code == 403

        # Test with no token, no credentials
        result = client.get("/secure-endpoint", timeout = 1)
        # Expecting 401 - Unauthorized
        assert result.status_code == 401

        # Test with no token, with credentials
        #result = requests.get(SERVER_URL+"/secure-endpoint", json={'user_name':'John Doe','password':'1234'}, timeout = 1)
        # Expecting 200 - OK
        #assert(result.status_code == 200)

    def run_project(self):
        # Create user
        client.post(
            "/user",
            json={'user_name': 'John Doe', 'password': '1234'},
            timeout=1
        )
        # Get user token
        token = client.post('/token', json={'user_name':'John Doe','password':'1234'}, timeout=1).json()['access_token']
    
        # Read project
        try:
            responce = client.get(
                "/project/myproject",
                headers={"Authorization": f"Bearer {token}"},
                timeout=1
            )
        except Exception:
            pass
        
        # Delete project
        responce = client.delete(
            "/project/myproject",
            headers={"Authorization": f"Bearer {token}"},
            timeout=1
        )
        # Create project
        responce = client.post(
            "/project/myproject",
            headers={"Authorization": f"Bearer {token}"},
            timeout=1
        )
        project_id = responce.json()['project_id']
        # Add file to project

        # Run project
        responce = client.post(
            "/run/"+project_id,
            headers={"Authorization": f"Bearer {token}"},
            timeout=1
        )
        result_id = responce.text
        responce = client.post(
            "/result",
            json={'result_id': result_id},
            headers={"Authorization": f"Bearer {token}"},
            timeout=1
        )

if __name__ == "__main__":
    john = TestExampleUser()
    token = john.test_login_process()
    john.use_token(token)
    john.run_project()
