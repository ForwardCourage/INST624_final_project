import requests
import json

api_url = 'https://meowfacts.herokuapp.com/'
api_resp = requests.get(api_url)
api_content = json.loads(api_resp.content)
api_content['data'][0]
class MeowApiCaller:

    def __init__(self, num) -> None:
        self.facts = []


    def get_facts(self, num):
        for i in range(num):
            resp = requests.get(api_url)
            content = json.loads(resp.content)
            fact = content['data'][0]
            self.facts.append(fact)

    def return_facts(self):
        return self.facts

    def cleanup(self):
        self.facts = []

    def getFactsNum(self):
        return len(self.facts)

