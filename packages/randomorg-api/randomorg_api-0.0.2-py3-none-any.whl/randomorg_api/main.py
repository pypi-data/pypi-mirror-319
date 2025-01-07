import requests
from typing import Union, List

url = "https://api.random.org/json-rpc/4/invoke"

class RangeTooNarrowError(Exception):
    def __init__(self, message):
        super().__init__(message)
    

class Generator():
    def __init__(self, RANDOM_ORG_API_KEY):
        self.apikey = RANDOM_ORG_API_KEY

    def randint(self, minimum=1, maximum=100, numofints=1, allowduplicates = True) -> Union[int, List[int]]:

        '''
        generates a random integer between min and max.
        default settings (no arguments) will generate one number between 1 to 100
        '''

        if not allowduplicates and numofints <= (maximum - minimum):
            raise RangeTooNarrowError("Range of numbers should be more than or equal to numofints when allowduplicates is set to true.")
        
        if minimum >= maximum:
            raise ValueError("min should be less than max")
        
        if numofints <= 0:
            raise ValueError("numofints should be positive")

        payload = {
            "jsonrpc": "2.0",
            "method": "generateIntegers",
            "params": {
                "apiKey": self.apikey,
                "n": numofints,
                "min": minimum,
                "max": maximum,
                "replacement": allowduplicates
            },
            "id": 1
        }

        try: 
            response = requests.post(url, json=payload)
            response.raise_for_status()

            result = response.json()

            if "error" in result:
                raise RuntimeError(f"{result['error']['message']} (error code {result['error']['code']})")

            return result['result']['random']['data']
        
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {str(e)}")
        
        except KeyError as e:
            raise RuntimeError(f"Unexpected API response structure: {response.json()}. Open an issue at http://github.com/ellipticobj/random-module and include this error.")
