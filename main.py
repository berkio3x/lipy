import sys
import logging
from optparse import OptionParser
from pprint import pformat
import math
import operator as OP
from functools import reduce

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


def tokenize(source):
    tokens = source.replace(')' ,' ) ').replace('(',' ( ').split()
    logger.debug(pformat(tokens))
    return tokens
    
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
        return eval_exp_tree(self.body, Environment(
            params=self.params, 
            args=args, 
            enclosing=self.env
            )
        )

def std_env():
    env = Environment()
    env.update(vars(math))
    env.update({
        '+': lambda *args: reduce(OP.add, args) ,
        '-': OP.sub    ,
        '*': OP.mul,#lambda *args: reduce(OP.mul,)
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
        'cons': lambda x,y:[x] + y,
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'append': OP.add,
        'length': len,
        'equal?': OP.eq,
        'begin': lambda *x: x[-1],
        'print': print
        
        })
    return env


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except:
            return str(token)
        
       
global_env = std_env()

def eval_exp_tree(exp, env=global_env):
    logger.debug(pformat(exp))
   
    if options.showenv:
        logger.debug(f'Evaluating expression with env: {pformat(env)}') 
    match exp:
        
        case int(exp):
            return exp 
        
        case ['quote', args]:
            return args[0]
        
        case ['set!', symbol, expression]:
            val = eval_exp_tree(expression, env)
            env.find_ref(symbol)[symbol] = val
            
        case ['lambda', args, body]:
            return Procedure(args, body,  env)
            
        case ['if', _, _, _]:
            (_, test, result, alt) = exp
            exp = (result if eval_exp_tree(test, env) else alt)
            return eval_exp_tree(exp, env)
        
        case ['define', _, _]:
            (_, symbol, expression) = exp
            env[symbol] = eval_exp_tree(expression, env)
        
        case str(exp):
            return env.find_ref(exp)[exp]
        
        case _ if exp:
            proc = eval_exp_tree(exp[0], env)
            args = [eval_exp_tree(arg, env) for arg in exp[1:]]
            return proc(*args)
    
def read_source(source):
    with open(source) as f:
        return f.read()
   
def execute_program(source, file=True):
    if file:
        source = read_source(prog_file)
    parsed = parse(tokenize(source))
    logger.debug('Parsed ast:')
    logger.debug(pformat(parsed))
    logger.debug('\n\n\nEvaluation steps\n\n\n')
    result = eval_exp_tree(parsed)
    return result

if __name__ == "__main__":
    prog_file = sys.argv[1]
    result = execute_program(prog_file)
    print(result)
    
