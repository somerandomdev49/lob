
class LangError(Exception):
    def __init__(self, e, msg):
        if e is None:
            super().__init__(msg)
        else:
            super().__init__(msg + ", but got '" + str(e.peek()) + "'")

token_types = {
    '+': 'Add',
    '-': 'Sub',
    '*': 'Mul',
    '/': 'Div',
    '%': 'Mod',
    '^': 'Pow',
    ',': 'Comma',
    '(': 'Open',
    ')': 'Close',
    '{': 'OpenCurly',
    '}': 'CloseCurly',
    '>': 'Greater',
    '<': 'Less',
    '|': 'Or',
    '&': 'And',
    '.': 'Dot',
    ';': 'Semi',
    '[': 'OpenSquare',
    ']': 'CloseSquare'
}

operator_map = {
    'Add': lambda x, y: x + y,
    'Sub': lambda x, y: x - y,
    'Mul': lambda x, y: x * y,
    'Div': lambda x, y: x / y,
    'Mod': lambda x, y: x % y,
    'Pow': lambda x, y: x ** y,
    'Same': lambda x, y: x == y,
    'Or': lambda x, y: x or y,
    'And': lambda x, y: x and y,
    'Less': lambda x, y: x < y,
    'Greater': lambda x, y: x > y,
}

class Lexer:
    def __init__(self, s):
        self.s = s

    def peek(self):
        if len(self.s) == 0:
            return '\0'
        return self.s[0]
    
    def next(self):
        x = self.peek()
        self.s = self.s[1:]
        return x

    def trim(self):
        while self.peek().isspace():
            self.next()

    def get_token(self):
        self.trim()
        if self.peek().isdigit():
            s = ""
            while self.peek().isdigit():
                s += self.next()
            return ('Num', float(s))

        elif self.peek().isalpha() or self.peek() == '_':
            s = ""
            while self.peek().isalnum() or self.peek() == '_':
                s += self.next()
            return ('Var', s)
        
        elif self.peek() == '"':
            self.next()
            s = ""
            while self.peek() != '"':
                s += self.next()
            self.next()
            return ('Str', s)

        elif self.peek() == '=':
            v = self.next()
            if self.peek() == '=':
                return ('Same', v + self.next())
            return ('Equals', v)

        elif self.peek() in token_types:
            return (token_types[self.peek()], self.next())
       
        elif self.peek() == '\0':
           return ('EOF', '\0')

        else:
            raise LangError(None,
                "Unknown character: '" + self.peek() + "' (" +
                            str(ord(self.next())) + ")")
    
    def get_tokens(self):
        vs = []
        while len(self.s) != 0:
            vs.append(self.get_token())
        return vs

class Parser:
    def __init__(self, ts):
        self.ts = ts
    
    def peek(self):
        if len(self.ts) == 0:
            return ("EOF", "\0")
        return self.ts[0]

    def next(self):
        x = self.peek()
        self.ts = self.ts[1:]
        return x

    def parse_atom(self):
        if self.peek()[0] == 'Open':
            self.next()
            e = self.parse_expr()
            if self.peek()[0] != 'Close':
                raise LangError(self, "Expected ')'")
            self.next()
            return e
        
        if self.peek()[0] == 'OpenSquare':
            return ('List',
                self.parse_arguments(False, 'OpenSquare', 'CloseSquare'))

        if self.peek()[0] == 'OpenCurly':
            self.next()
            x = self.peek()[0] == 'Or'
            args = None
            if x: args = self.parse_arguments(True, 'Or', 'Or')
            v = self.parse_stmts()
            if self.peek()[0] != 'CloseCurly':
                raise LangError(self, "Expected '}'")
            self.next()
            return ('Func', v, args) if x else v

        elif self.peek()[0] == 'Num':
            return self.next()

        elif self.peek()[0] == 'Var':
            return self.next()

        elif self.peek()[0] == 'Str':
            return self.next()
        
        else:
            raise LangError(self, "Expected a number, name or string")

    def parse_arguments(self,
            var_only = False,
            p_o = 'Open',
            p_c = 'Close',
            p_d = 'Comma'):
        if self.peek()[0] != p_o:
            raise LangError(self, "Expected '('")
        self.next()

        if self.peek()[0] == p_c:
            self.next()
            return []

        args = []
        if var_only:
            if self.peek()[0] != 'Var':
                raise LangError(self, "Expected a name")
            args.append(self.next()[1])
        else:
            args.append(self.parse_expr())
        while self.peek()[0] == p_d:
            self.next()
            if var_only:
                if self.peek()[0] != 'Var':
                    raise LangError(self, "Expected a name")
                args.append(self.next()[1])
            else:
                args.append(self.parse_expr())
        if self.peek()[0] != p_c:
            raise LangError(self, "Expected closing")
        self.next()
        return args

    def parse_molecule(self):
        a = self.parse_atom()
        while self.peek()[0] == 'Open' or self.peek()[0] == 'Dot':
            if self.peek()[0] == 'Open':
                args = self.parse_arguments()
                return ('Call', a, args)
            if self.peek()[0] == 'Dot':
                self.next()
                if self.peek()[0] != 'Var':
                    raise LangError(self, "Expected a name")
                a = ('Dot', a, self.next()[1])
        return a

    def parse_mul(self):
        o = self.parse_molecule()
        while self.peek()[0] == 'Mul' or self.peek()[0] == 'Div':
            n = self.next()[0]
            o = (n, o, self.parse_molecule())
        return o
    
    def parse_add(self):
        o = self.parse_mul()
        while self.peek()[0] == 'Add' or self.peek()[0] == 'Sub':
            n = self.next()[0]
            o = (n, o, self.parse_mul())
        return o
    
    def parse_comparison(self):
        o = self.parse_add()
        while self.peek()[0] == 'Less' or self.peek()[0] == 'Greater':
            n = self.next()[0]
            o = (n, o, self.parse_add())
        return o
    
    def parse_equality(self):
        o = self.parse_comparison()
        while self.peek()[0] == 'Same':
            n = self.next()[0]
            o = (n, o, self.parse_comparison())
        return o
    
    def parse_assign(self):
        o = self.parse_equality()
        if o[0] != 'Var': return o
        if self.peek()[0] == 'Equals':
            self.next()
            o = ("Assign", o[1], self.parse_equality())
        return o
    
    def parse_expr(self):
        o = []
        if self.peek()[1] == 'import':
            self.next()
            n = self.peek()[1]
            if self.peek()[0] != 'Var':
                raise LangError(self, "Expected a name")
            self.next()
            x = None
            if self.peek()[1] == 'as':
                self.next()
                x = self.peek()[1]
                if self.peek()[0] != 'Var':
                    raise LangError(self, "Expected a name")
                self.next()
            return ('Import', n, x)
        elif self.peek()[1] == 'if':
            self.next()
            e = self.parse_expr()
            v = self.parse_expr()
            k = None
            if self.peek()[1] == 'else':
                self.next()
                k = self.parse_expr()
            return ('If', e, v, k)
        elif self.peek()[1] == 'for':
            self.next()

            n = self.peek()[1]

            if self.peek()[0] != 'Var':
                raise LangError(self, "Expected a name")
            self.next()

            if self.peek()[0] != 'Open':
                raise LangError(self, "Expected '('")
            self.next()

            v = self.parse_expr()

            if self.peek()[0] != 'Close':
                raise LangError(self, "Expected ')'")
            self.next()

            x = self.parse_expr()
            
            return ('For', n, v, x)
        else:
            return self.parse_assign()
        
    def parse_stmts(self):
        l = [self.parse_expr()]
        while self.peek()[0] == 'Semi':
            self.next()
            l.append(self.parse_expr())
        return ('Sequence', l)

class Eval:
    def __init__(self, parent = None):
        self.parent = parent
        self.c = {}
    
    def __getitem__(self, name):
        if name in self.c:
            return self.c[name]
        if self.parent is not None:
            return self.parent[name]
        raise LangError(None, "No such variable: '" + name + "'")

    def __setitem__(self, name, value):
        if name in self.c:
            self.c[name] = value
        if self.parent is not None and name in self.parent:
            self.parent[name] = value
        self.c[name] = value

    def __contains__(self, name):
        if name in self.c: return True
        if self.parent is not None: return name in self.parent
        return False
    
    def import_module(self, name, alias=None):
        _name = name
        if alias is not None:
            name = alias
        if name in self.c:
            raise LangError(None, "Cannot import module as " + name +
                ": there is already a variable the same name.")
        evl = Eval(self)
        run_file(_name + ".lob", evl)
        self.c[name] = evl.c
    
    def eval_node(self, n):
        if n is None: return None
        if n[0] in operator_map:
            return operator_map[n[0]](
                self.eval_node(n[1]),
                self.eval_node(n[2]))
        if n[0] == 'Num':
            return n[1]
        if n[0] == 'Var':
            return self[n[1]]
        if n[0] == 'Str':
            return n[1]
        if n[0] == 'List':
            return [self.eval_node(x) for x in n[1]]
        if n[0] == 'Call':
            return self.eval_node(n[1])\
                (*[self.eval_node(x) for x in n[2]])
        if n[0] == 'Assign':
            self[n[1]] = self.eval_node(n[2])
            return self[n[1]]
        if n[0] == 'Import':
            return self.import_module(n[1], n[2])
        if n[0] == 'If':
            evl = Eval(self)
            return evl.eval_node(n[2]) if\
                self.eval_node(n[1]) else evl.eval_node(n[3])
        if n[0] == 'For':
            x = None
            evl = Eval(self)
            for e in self.eval_node(n[2]):
                evl.c[n[1]] = e
                x = evl.eval_node(n[3])
            return x
        if n[0] == 'Func':
            def inner(*args):
                evl = Eval(self)
                for name, val in zip(n[2], args):
                    evl.c[name] = val # .c is important!
                return evl.eval_node(n[1])
            return inner
        if n[0] == 'Sequence':
            l = None
            for e in n[1]:
                l = self.eval_node(e)
            return l
        if n[0] == 'Dot':
            try:
                return self.eval_node(n[1])[n[2]]
            except KeyError:
                raise LangError(None, "No such field: " + n[2])
        raise LangError(None, "Unsopported node: " + n[0])

class StdEval(Eval):
    def __init__(self):
        self.parent = None
        self.c = {
            'print': print,
            'input': input,
            'int': int,
            'float': float,
            'exit': exit,
            'eval': lambda x: run_expr(x, self),
            'clear': clear,
            'import': self.import_module,
            'len': len,
            '__py_exec__': self.py_exec
        }
    
    def py_exec(self, s):
        loc = {}
        exec(s, {}, loc)
        return loc["__res"]



# https://stackoverflow.com/a/44591228/9110517
import os
def clear():
    os.system('cls||printf "\\\\033c"')

def run_expr(s, e):
    lex = Lexer(s)
    par = Parser(lex.get_tokens())
    x = par.parse_stmts()
    if par.peek()[0] != 'EOF':
        raise LangError(par, 'Expected EOF')
    return e.eval_node(x)

def run_file(s, e):
    with open(s, "r") as f:
        return run_expr(f.read(), e)

evl = Eval(StdEval())
while True:
    try:
        x = input('❮ ')
        if x: print('❯ ' + str(run_expr(x, evl)))
    except LangError as e:
        print("⌀ Error:", e)
