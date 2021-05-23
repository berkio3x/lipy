import sys
import logging
from optparse import OptionParser
from pprint import pformat
import math
import operator as OP
from functools import reduce
from typing import List

parser = OptionParser()

parser.add_option("-l" , "--loglevel" , 
                  dest = "loglevel" ,
                  default =logging.INFO
                  )

parser.add_option("-e", "--showenv",
                  dest ="showenv" , 
                  default = False
                  )
(options, args) = parser.parse_args()

logging.basicConfig(format='[Line: %(lineno)d] %(message)s \n',
                    datefmt='%Y-%m-%d:%H:%M:%S')


logger = logging.getLogger(__name__)
if options.loglevel == "debug":
        options.loglevel = logging.DEBUG
        
logger.setLevel(options.loglevel)


def isnum(num):
    try:
        int(num)
    except ValueError:
        try:
            float(num)
        except ValueError:
            return False
    return True 



class Symbol(str):
    def __repr__(self):
        return f'<symbol {self}>'
    

_symbols = ('set!', 'define' ,'quote', 'if' , 'else' ,'begin', 'lambda' )
symbol_table = { s: Symbol(s) for s in _symbols}

# Define symbols
_set = Symbol('set!')
_define = Symbol('define')
_quote = Symbol('quote')
_if = Symbol('if')
_else = Symbol('else')
_begin = Symbol('begin')
_lambda = Symbol('lambda')

end_of_file = Symbol('<# end-of-file>')

class Tokenizer:

    def __init__(self, source):
        self.source = source
        self.c = 0
        self.start = 0
        self.operators = ('+' ,'-', '*', '/')
        self.tokens = []
    
    def error(self, ch):
        raise SyntaxError(f'Unrecognized token: {ch}')
        
    def next(self) -> str:
        self.c += 1
        return self.source[self.c - 1]

    def peek(self) -> str:
        return self.source[self.c]

    def tokenize(self) -> List:
        tokens = self.scan_tokens()
        return self.tokens
    
    def end_of_source(self) -> bool:
        return self.c >= len(self.source)

    def read_token(self) -> List:
        #import pdb;pdb.set_trace()
        ch = self.next()
        #print(ch)

        if ch == "=":
            tokens.append(ch)
        
        elif ch == "(" or ch == ")":
            self.tokens.append(ch)
            
        elif ch == ">":
            if self.peek() == '=':
                self.tokens.append('>=')
                self.next()
            else:
                self.tokens.append('>')
            
        elif ch == "<":
            if self.peek() == '=':
                self.tokens.append('<=')
                self.next()
            else:
                self.tokens.append('<')

        elif ch == ";":
            while self.peek() and self.peek() != '\n':
                self.next()
                
        elif isnum(ch):
            while self.peek() and isnum(self.peek()):
                self.next()
            num = self.source[self.start: self.c]
            self.tokens.append(num)
           
        elif ch == '"':
            while self.peek() and self.peek() != '"':
                self.next()
            # consume the last "
            self.next()
            _token = self.source[self.start: self.c]
            self.tokens.append('"'+_token+'"')
            
        elif ch.isalpha():
            while ( self.peek().isalpha()  
            or self.peek() == '-' 
            or self.peek() == '!' 
            or self.peek() == '?'):
                self.next()
            _token = self.source[self.start: self.c]
            self.tokens.append(_token)
            
        elif ch in self.operators:
            self.tokens.append(ch)
        elif ch == ' ':
            pass
        else:
            self.error(ch)
    
    def scan_tokens(self):
        while not self.end_of_source():
            self.start = self.c
            self.read_token()

def parse(tokens):
    if not tokens:
        print('No input source')
    token = tokens.pop(0)
    if token == '(':
        L  = []
        while tokens[0] != ')':
            _token = parse(tokens)
            L.append(_token)
        tokens.pop(0)
        return L
    elif token == ')':
        print('Unexpected `)`')
    else:
        return atom(token)




# Class to keep track of scope
class Environment(dict):
    def __init__(self, params=(), args=(), enclosing=None):
        self.update(zip(params, args))
        self.enclosing = enclosing
    
    def find_ref(self, key):
        if key in self:
            return self
        else:
            if self.enclosing:
                return self.enclosing.find_ref(key)



class Procedure:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env
    def __call__(self, *args):
        e = Environment(
            params=self.params,
            args=args,
            enclosing=self.env)
        
        for index, body in enumerate(self.body):
            res = eval_exp_tree(body, e)
            if index == len(self.body) - 1:
                return res
            
    
    
def set_break():
    import pdb;pdb.set_trace()

def python_bool_to_lisp_bool(value):
    if value == True:
        return '#t'
    if value == False:
        return '#f'
    
def lisp_bool_to_python_bool(value):
    if value == '#t':
        return True
    if value == '#f':
        return False
    
def custom_print(x):
    print(x)
    return x

def std_env():
    env = Environment()
    env.update(vars(math))
    env.update({
        '+': lambda *args: reduce(OP.add, args) ,
        '-': OP.sub    ,
        '*': lambda *args: reduce(OP.mul, args),
        '/': OP.truediv,
        '<': OP.lt     ,
        '>': OP.gt     ,
        '<=': OP.le    ,
        '>=': OP.add   ,
        '=': OP.eq     ,
        'not': lambda x: not x,
        'boolean?': lambda x: isinstance(x,bool),
        'number?': lambda x: isinstance(x,int),
        'expt': math.pow,
        'max': max,
        'min': min,
        'list-ref': lambda l, i: l[i],
        'list': lambda *x: list(x),
        'cons': lambda x,y:[x] + list(y),
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'append': OP.add,
        'length': len,
        'equal?': OP.eq,
        'begin': lambda *x: x[-1],
        'print': custom_print, 
        'string?': lambda x: python_bool_to_lisp_bool(isinstance(x, str)),
        'string-len': lambda s: len(s)-2,
        'string-ref': lambda s,k: s[k+1],
        
        })
    return env


def atom(token):
    if token == '#t': return True
    elif token == '#f': return False
    elif token[0] == '"' :return token[1:-1]
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except:
            return Symbol(token)

        
       
global_env = std_env()

def eval_exp_tree(exp, env=global_env):
    logger.debug(pformat(exp))
   
    if options.showenv:
        logger.debug(f'Evaluating expression with env: {pformat(env)}')

    #import pdb;pdb.set_trace();

    match exp:
        
        case Symbol(exp):
            logger.debug('variable refrencing')
            logger.debug(pformat(exp))
            return env.find_ref(exp)[exp]

        case str(exp):
            return exp
        
        case int(exp):
            logger.debug('int evaluation')
            return exp 
        
        case [Symbol('quote'), args]:
            return args[0]
        
        case [Symbol('set!'), symbol, expression]:
            
            logger.debug('<set! expression')
            logger.debug(symbol, expression)

            val = eval_exp_tree(expression, env)
            env.find_ref(symbol)[symbol] = val
            
        case [Symbol('lambda') , args, *body]:
            logger.debug('<lmbda procedure>')
            logger.debug(args, body)
            
            return Procedure(args, body,  env)
            
        case [Symbol('if'), test, result, alt]:
            logger.debug('<if condition evaluation>')
            logger.debug((test, result, alt))
            
            exp = (result if eval_exp_tree(test, env) else alt)
            return eval_exp_tree(exp, env)
        
        case [Symbol('define'), symbol, expression]:
            logger.debug('<define variable>')
            logger.debug(symbol, expression)
            env[symbol] = eval_exp_tree(expression, env)
        
        
        case _ if exp:
            logger.debug('<procedure call>')
            proc = eval_exp_tree(exp[0], env)
            args = [eval_exp_tree(arg, env) for arg in exp[1:]]
            #print(proc, args)
            return proc(*args)
    
def read_source(source):
    with open(source) as f:
        return f.read()
   
def execute_program(source, file=True):
    if file:
        source = read_source(prog_file)
    t = Tokenizer(source)
    tokens  = t.tokenize()
    parsed = parse(tokens)
    logger.debug('Parsed ast:')
    logger.debug(pformat(parsed))
    logger.debug('\n\n\nEvaluation steps\n\n\n')
    result = eval_exp_tree(parsed)
    return result


def repl():
    while True:
        expr = input(">>>")
        if expr == "(exit)": break 
        if expr.strip() == "": continue
        try:
            res = execute_program(expr, file=False)
            print(res)
        except Exception as e:
            print(str(e))
        
    
if __name__ == "__main__":
    prog_file = sys.argv[1]
    result = execute_program(prog_file)
    print(result)
    
