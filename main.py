# Shunting-yard algorithm based math expression evaluator.
# Made by somerandomdev49. MIT License.


# Name: (Precedence, Left Associative)
operators = {
    "+": (2, True),
    "-": (2, True),
    "*": (4, True),
    "/": (4, True),
    "^": (6, False),
    "$": (100, False)
}

def paser_expr(s):
    ts = s.split()
    v, o = [], []
    while len(ts) != 0:
        t = ts[0]
        ts = ts[1:]
        if t in operators:
            x = operators[t]
            while len(o) != 0 and t in o[-1] in operators and\
                (operators[t][0] < operators[o[-1]][0] or
                (operators[t][1] and
                    operators[t][0] == operators[o[-1]][0])):
                v.append(o.pop())
            o.append(t)
        elif t == '(':
            o.append(t)
        elif t == ')':
            while o[-1] != '(':
                v.append(o.pop())
                if len(o) == 0:
                    raise Exception("Mismatched parenthesis.")
            if o[-1] == '(':
                o.pop()
        else:
            v.append(t)
    if len(o) != 0:
        v.extend(reversed(o))
    return v

def eval_expr(es):
    print("Eval:", es)
    s = []
    for e in es:
        if e in operators:
            b, a = s.pop(), s.pop()
            if False: pass # alignment
            elif e == '+': s.append(a + b)
            elif e == '-': s.append(a - b)
            elif e == '*': s.append(a * b)
            elif e == '/': s.append(a / b)
            elif e == '^': s.append(a ** b)
        else: s.append(float(e))
    return s[-1]


print('❯ ' + str(eval_expr(paser_expr(input('❮ ')))))
