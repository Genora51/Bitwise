from lib.bitparser import Parse
from lib.lexer import lex
from lib.basefuncs import Token, tokens
import os
from lib.evaluator import runStates as evaluate
import hashlib

def h11(w):
    return hashlib.md5(w.encode()).hexdigest()[:9]

def interpret(text, vals = None):
	lexed = lex(text, tokens)
	parsed = Parse(lexed)
	if vals is None:
		return evaluate(parsed)
	else: return evaluate(parsed,vals)

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

def runCmd(args):
	runFile(args.program)
	if args.inputend:
		input('Press enter to continue...')

def shell(args):
	ext = False
	sysex = False
	vs = None
	print("Bitwise Shell")
	print("-"*20)
	while not ext:
		if sysex:
			sysex = False
			inp = input('\n-> ')
		else:
			inp = input('-> ')
		ext = inp == "exit"
		try:
			if not ext:
				if vs is not None:
					vs = interpret(inp)
				else: vs = interpret(inp, vs)
		except SystemExit:
			sysex = True

if __name__ == '__main__':
	import argparse

	# ...
	parser = argparse.ArgumentParser(
	    description="Interpreter for the Bitwise Language."
	)
	
	pars = parser.add_subparsers()
	rg = pars.add_parser('run', help='Run a Bitwise (.bit) program.')
	rg.add_argument(
	    "-i",
	    "--inputend",
	    action="store_true",
	    help="Whether to end the program with a pause."
	)
	rg.add_argument(
	    "program",
	    help="The path of the program to be run."
	)
	rg.set_defaults(func=runCmd)
	sg = pars.add_parser('shell', help="Run a Bitwise shell.")
	sg.set_defaults(func=shell)
	args = parser.parse_args()
	try:
		args.func(args)
	except AttributeError:
		args = parser.parse_args(['-h'])