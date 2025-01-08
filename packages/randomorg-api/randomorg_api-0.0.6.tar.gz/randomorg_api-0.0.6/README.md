# random
a python module to get random numbers from random.org

## basic implementation
install the module
```bash
pip3 install randomorg_api
```

import the module 
```python
from randomorg_api import Generator
```

initialize the generator 
```python
randomgen = Generator(apikey = "API_KEY_HERE")
```

generate a number

```python
randomgen.randint()
```

## roadmap
add .dice() or .d6(), etc 
add .choice()
add .string()

for documentation go [here](http://github.com/ellipticobj/random-module/DOCUMENTATION.md)

