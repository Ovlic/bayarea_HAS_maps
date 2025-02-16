import requests

class MySession:
    def __init__(self, key):
        self.session = requests.Session()
        self.session.params["api_key"] = key

    def get(self, url, **kwargs):
        response = self.session.get(url, **kwargs)
        #print(response.status_code)
        return self.status_handler(response)
    
    def status_handler(self, response):
        if response.status_code == 200:
            return response
        else:
            raise requests.exceptions.HTTPError(f"Bad response: {response.status_code}")
