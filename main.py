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

logging.basicConfig()
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


def std_env():
    env = dict()
    env.update(vars(math))
    env.update({
        '+': OP.add    ,
        '-': OP.sub    ,
        '*': OP.mul    ,
        '/': OP.truediv,
        '<': OP.lt     ,
        '>': OP.gt     ,
        '<=': OP.le    ,
        '>=': OP.add   ,
        '=': OP.eq     ,
        'append': OP.add,
        'length': len,
        'equal?': OP.eq,
        'begin': lambda *x: x[-1],
        
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
    logger.debug(exp)
   
    if options.showenv:
        logger.debug(f'Evaluating expression with env: {pformat(env)}') 
    match exp:
        case str(exp):
            return env[exp]
        case int(exp):
            return exp 
        case ['if',_,_,_]:
            (_, test, result, alt) = exp
            exp = (result if eval_exp_tree(test, env) else alt)
            return eval_exp_tree(exp, env)
        case ['define',_,_]:
            (_, symbol, expression) = exp
            env[symbol] = eval_exp_tree(expression, env)
        case _ if exp:
            proc = eval_exp_tree(exp[0], env)
            args = [eval_exp_tree(arg, env) for arg in exp[1:]]
            return proc(*args)
    
def read_source(source):
    with open(source) as f:
        return f.read()
    
if __name__ == "__main__":
    prog_file = sys.argv[1]
    source = read_source(prog_file)
    parsed = parse(tokenize(source))
    logger.debug('Parsed ast:')
    logger.debug(parsed)
    logger.debug('Evaluation steps')
    result = eval_exp_tree(parsed)
    print(result)
    
