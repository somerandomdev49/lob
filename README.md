# Lob
not an acronym, just something.

`main2.py` is the main file, `main.py` is just me experimenting.

## Example:
```c++

id = { (a) a };

MAX_NUMBER = __py_exec__("import sys; __res = sys.float_info.max");
MIN_NUMBER = __py_exec__("import sys; __res = sys.float_info.min");

min = { (l)
    m = MAX_NUMBER;
    for i(l) (
        if i < m
            m = i
    ); m
};

max = { (l)
    m = MIN_NUMBER;
    for i(l) (
        if i > m
            m = i
    ); m
}


```

## Syntax:

### Operators:
`+, -, /, *, ^ (power), %, | (or), & (and), == (equal?)`

### Functions:
Function call: `name(..., ..., ..., ...)`
Function expression: `{ (a, b, c, ...) ... }`

### Lists:
List: `[ ..., ..., ... ]`

### Modules
Import: `import name` (imports `./name.lob` into `name` variable)
> TODO
> Import as: `import name as alias` (imports `./name.lob` into `alias` variable)

### Variables
Access: `name.a.b.c.d`
Assign / Define: `name = ...`

### For loop:
For loop: `for item(list) ...`

### If:
If: `if ... ... `
If else: `if ... ... else ...`
