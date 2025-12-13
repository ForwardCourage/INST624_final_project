import requests
import json

api_url = 'https://meowfacts.herokuapp.com/'
# api_resp = requests.get(api_url)
# api_content = json.loads(api_resp.content)
# api_content['data'][0]
class MeowApiCaller:

    def __init__(self) -> None:
        self.facts = []
        self.length = 0

    def updateLen(self):
        self.length = len(self.facts)


    def getFacts(self, num):
        api_with_count = f'{api_url}/?count={num}'
        resp = requests.get(api_with_count)
        content = json.loads(resp.content)
        self.facts = content['data']
        self.updateLen()
    
    def printFacts(self, num):

        for i in range(min(num, self.returnLen())):
            print(self.facts[i])


    def returnFacts(self):
        return self.facts
    
    def returnLen(self):
        return self.length

    def cleanUp(self):
        self.facts = []
        self.updateLen()

    

if __name__ == '__main__':
    caller = MeowApiCaller()
    caller.getFacts(10)
    caller.printFacts(15)
