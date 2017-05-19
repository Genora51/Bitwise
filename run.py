from bitwise.bitparser import Parse
from bitwise.lexer import lex
from bitwise.basefuncs import Token
import os
from bitwise.evaluator import runStates as evaluate

def interpret(text):
	lexed = lex(text)
	parsed = Parse(lexed)
	evaluate(parsed)

def runFile(fileName):
	dirf = os.path.dirname(os.path.realpath(fileName))
	cach = "%s/__bitcache__/%sc"%(dirf,fileName)
	if os.path.isfile(cach):
		parsed = eval(open(cach).read())
	else:
		lexed = lex(open(fileName).read())
		parsed = Parse(lexed)
		with open(cach,'w') as f:
			f.write(repr(parsed))
	evaluate(parsed)