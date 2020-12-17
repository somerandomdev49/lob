# Lob
not an acronym, just something.

`main2.py` is the main file, `main.py` is just me experimenting.

## Example:
```ruby
id = { |a| a };

min = { |l|
    m = MAX_NUMBER;
    for i(l) (
        if i < m
            m = i
    ); m
};

max = { |l|
    m = MIN_NUMBER;
    for i(l) (
        if i > m
            m = i
    ); m
};

sum = { |l|
    s = 0;
    for i(l) s = s + i;
    s
};

avg = { |l|
    sum(l) / len(l)
}

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
