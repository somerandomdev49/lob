# Lob
not an acronym, just something.

`lob.py` is the main file

## Example:
```ruby
import math;
a = float(input());
b = float(input());
c = float(input());

p = (a + b + c) / 2;

print(math.sqrt(p * (p - a) * (p - b) * (p - c)))
```

## Syntax:

### Operators:
`+, -, /, *, ^ (power), %, | (or), & (and), == (equal?)`

### Functions:
* Statement list: 
* Function call: `name(..., ..., ..., ...)`
* Function expression: `{ |a, b, c, ...| ... }`

### Lists:
* List: `[ ..., ..., ... ]`

### Modules
* Import: `import name` (imports `./name.lob` into `name` variable)

* `import name as alias` (imports `./name.lob` into `alias` variable)

### Variables
* Access: `name.a.b.c.d`
* Assign / Define: `name = ...`

### For loop:
* For loop: `for item(list) ...`

### If:
* If: `if ... ... `
* If else: `if ... ... else ...`

## Built-ins
* `print(...)`: prints the arguments separated by a space
* `input([prompt])`: prompts the user for a string.
* `int(str)`: converts a string to an integer.
* `float(str)`: converts a string to an float,
* `exit()`: exits the program.
* `eval(code)`: runs code.
* `clear()`: clears the screen *useful if REPL is cluttered)
* `import(name)`: same as `import name`. `name` is a string.
* `len(cont)`: returns the length of a string or a list.
