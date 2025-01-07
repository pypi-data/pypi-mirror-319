# docs (not well made pluh!)

official documentatiol for this module

# quickstart

import the module 

```python
import randomorg_api as random
```

initialize the generator

```python
randgen = Generator(API_KEY_HERE)
```

# commands

## randint

randint generates a random integer  

### arguments

**minimum**
minimum number that can be generated (inclusive)  

**maximum**
maximum number that can be generated (inclusive)  
should be at least one more than minimum  

**numofints**
number of integers that are generated.  
should be positive  
default value is 1

**allowduplicates**
only applies when multiple numbers are generated  
when set to true, the numbers that are generated can contain duplicate numbers
default value is true


# exceptions
