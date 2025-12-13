import requests
import json

api_url = 'https://meowfacts.herokuapp.com/'
api_resp = requests.get(api_url)
api_content = json.loads(api_resp.content)

class MeowApiCaller:

    def __init__(self, num) -> None:
        self.facts = []
        self.num = num

    def get_facts(self):
        for i in range(self.num):
            pass
