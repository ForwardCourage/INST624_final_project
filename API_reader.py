import requests
import json
import random
api_url = 'https://meowfacts.herokuapp.com' # Meowfacts API url

class MeowApiCaller:
    """
    This is an API caller designed to get data from Meowfacts API.

    Meowfacts API is a very simple API that requires little data processing. 
    It can return facts about cats in a simple format.
    """

    def __init__(self) -> None:
        self.facts = []
        self.length = 0

    def updateLen(self):
        """ 
        This methods updates its length argument.
        """
        self.length = len(self.facts)


    def getFacts(self, num):
        """
        This method gets facts of appointed numbers from Meowfacts API
        """
        api_with_count = f'{api_url}/?count={num}'
        resp = requests.get(api_with_count)
        content = json.loads(resp.content)
        self.facts = content['data']
        self.updateLen()
    
    def printFacts(self, num: int) -> None:
        """
        Print a random subset of stored facts (no duplicates within one call).
        If num exceeds available facts, prints all facts in random order.
        """
        k = min(num, self.returnLen())
        for fact in random.sample(self.facts, k):
            print(fact)

    def returnFacts(self):
        return self.facts
    
    def returnLen(self):
        return self.length

    def cleanUp(self):
        """
        This method cleans up all facts stored in it and update the length.
        """
        self.facts = []
        self.updateLen()

    

    

if __name__ == '__main__':
    caller = MeowApiCaller()
    caller.getFacts(10)
    caller.printFacts(15)
