import requests
from typing import Union, List

url = "https://api.random.org/json-rpc/4/invoke"

def getint(apikey, numofints, minimum, maximum, allowduplicates):
    payload = {
            "jsonrpc": "2.0",
            "method": "generateInteger",
            "params": {
                "apiKey": apikey,
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
        raise RuntimeError(f"Unexpected API response structure: {response.json()}. Open an issue at http://github.com/ellipticobj/random-module/issues and include this error.")


def getstring(apikey, numofstrings, length, characters, allowduplicates):
    payload = {
        "jsonrpc": "2.0",
        "method": "generateStrings",
        "params": {
            "apiKey": apikey,
            "n": numofstrings,
            "length": length,
            "characters": characters,
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
        raise RuntimeError(f"Unexpected API response structure: {response.json()}. Open an issue at http://github.com/ellipticobj/random-module/issues and include this error.")

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
        
        return getint(self.apikey, numofints, minimum, maximum, allowduplicates)
        
    def dice(self, sides=6):
        
        '''
        rolls a dice with the specified number of sides
        '''
        
        return getint(self.apikey, 1, 1, sides, True)
    
    def string(self, numofstrings, length, allowduplicates, characters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        
        return getstring(self.apikey, numofstrings, length, characters, allowduplicates)

    def choice(self, seq):
        '''
        chooses a random item from a rist and returns it
        '''
        
        if not seq:
            raise ValueError("List cannot be empty.")
        
        randindex = getint(self.apikey, 1, 0, len(seq)-1,True)
        return seq[randindex]
    
    def shuffle(self, seq, modifyoriginal=True):
        '''
        shuffles items in a list and either returns the list or modifies the list
        '''
        
        if not seq:
            return
        
        randomindices = getint(self.apikey, len(seq), 0, len(seq)-1, False)
        
        shuffled = [seq[i] for i in randomindices]
        
        if modifyoriginal:
            seq[:] = shuffled
        else:
            return shuffled
        
    def random(self, decimals=10, numoffloats=1):
        '''
        randomly generates a float from 0 to 1
        '''
        
        if decimals <= 0:
            raise ValueError("Number of decimal places must be positive")
        
        payload = {
            "jsonrpc": "2.0",
            "method": "generateDecimalFractions",
            "params": {
                "apiKey": self.apikey,
                "n": numoffloats,
                "decimalPlaces": decimals
            },
            "id": 1
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()

            result = response.json()

            if "error" in result:
                raise RuntimeError(f"{result['error']['message']} (error code {result['error']['code']})")

            return float(result['result']['random']['data'][0])

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {str(e)}")

        except KeyError:
            raise RuntimeError(f"Unexpected API response structure: {response.json()}.")
        
    def coinflip(self, returnbool=False):
        '''
        flips a coin
        '''
        
        result = getint(self.apikey, 1, 0, 1, True)
        
        if returnbool:
            return bool(result)
        else:
            return "heads" if result else "tails"