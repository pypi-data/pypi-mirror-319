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

generates a random integer  

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

## dice

acts like a die

### arguments

**sides**
number of sides of the dice
default value is 6
should be a positive number

## string

generates a string of random characters

### arguments

**numofstrings**  
number of strings to be generated.  
has to be at positive  
  
**length**  
length of the string to be generated  
has to be positive  
  
**allowduplicates**  
whether duplicate strings can be generated  
  
**characters**  
characters that can be generated  
the default value is  
```
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
```

## choice

randomly picks an item in a list  

### arguments

**seq**  
the list to be picked from  
has to have at least one item  

## shuffle

randomly shuffles a list

### arguments

**seq**  
the list to shuffle  
  
**modifyoriginal**  
whether the function modifies the original list or returns the list
defaults to true

## random

returns a random float from 0 to 1

### arguments

**decimals**  
number of decimal places to generate  
defaults to 10  
  
**numoffloats**
number of floats to generate  
defaults to 1  

## coinflip

flips a coin
returns a boolean, or "heads" or "tails"

### arguments

**returnbool**  
returns a boolean if set to true, returns "heads" or "tails" otherwise  
set to false by default  

# exceptions
