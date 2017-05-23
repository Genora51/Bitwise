"""Bitwise.

Usage:
  bitwise [-i] PROGRAM
  bitwise --shell
  bitwise -h | --help
  bitwise --version


Options:
  -h --help      Show this screen.
  --version      Show version.
  -i --inputend  Whether to pause at the end.
  -s --shell     Run a Bitwise Shell

"""

from lib.bitparser import Parse
from lib.lexer import lex
from lib.basefuncs import Token, tokens, raiseErrN
import os
from lib.evaluator import runStates as evaluate, expEval
import hashlib

def h11(w):
	return hashlib.md5(w.encode()).hexdigest()[:9]

def interpret(text, vals = None):
	lexed = lex(text, tokens)
	parsed = Parse(lexed)
	if vals is None:
		return evaluate(parsed)
	else: return evaluate(parsed,vals)

def interpretExp(text, vals = None):
	interpret('<' + text, vals)

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
	runFile(args['PROGRAM'])
	if args['--inputend']:
		input('Press enter to continue...')

def shell(args):
	ext = False
	vs = None
	print("Bitwise Shell")
	print("-"*20)
	while not ext:
		inp = input('-> ')
		ext = inp == "exit"
		try:
			if not ext:
				if vs is not None:
					vs = interpret(inp)
				else: vs = interpret(inp, vs)
		except SystemExit as e:
			if e.args[0].startswith('ParserError: Unused '):
				try:
					interpretExp(inp,vs)
				except SystemExit as er:
					print(er.args[0])
			else:
				print(e.args[0])

if __name__ == '__main__':
	try:
		from docopt import docopt
	except ImportError:
		raiseErrN("You need docopt!\nInstall it from http://pypi.python.org/pypi/docopt\nor run pip install docopt.")

	arguments = docopt(__doc__, version='Bitwise 0.0.3')
	if arguments['--shell']:
		shell(arguments)
	else:
		runCmd(arguments)