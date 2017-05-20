from lib.bitparser import Parse
from lib.lexer import lex
from lib.basefuncs import Token, tokens
import os
from lib.evaluator import runStates as evaluate
import hashlib

def h11(w):
    return hashlib.md5(w.encode()).hexdigest()[:9]

def interpret(text):
	lexed = lex(text, tokens)
	parsed = Parse(lexed)
	evaluate(parsed)

def runFile(fileName):
	dirf = os.path.dirname(os.path.realpath(fileName))
	cach = r"%s\__bitcache__\%sc"%(dirf,os.path.basename(fileName))
	mtxt = open(fileName).read()
	if os.path.isfile(cach):
		hashed, ptext = open(cach).read().split('\n')
		if h11(mtxt) == hashed:
			parsed = eval(ptext)
		else:
			parsed = parsNo(mtxt,dirf,cach)
	else:
		parsed = parsNo(mtxt,dirf,cach)
	evaluate(parsed)

def parsNo(mtxt,dirs,cach):
	try:
		os.mkdir(dirs + r"\__bitcache__")
	except OSError:
		pass
	lexed = lex(mtxt, tokens)
	parsed = Parse(lexed)
	with open(cach,'w') as f:
		pt = repr(parsed)
		f.write(h11(mtxt) + '\n')
		f.write(pt)
	return parsed

if __name__ == '__main__':
	import argparse
	# ...
	parser = argparse.ArgumentParser(
	    description="Runs a Bitwise (.bit) program."
	)
	parser.add_argument(
	    "program",
	    help="The path of the program to be run."
	)

	args = parser.parse_args()
	runFile(args.program)
	input('Press any key to continue...')
