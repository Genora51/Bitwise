from basefuncs import *
from functional import compose

class FunctionalFunction(object):
	def __init__(self, func):
		self.func = func
	def __call__(self, *args, **kwargs):
		return self.func(*args, **kwargs)
	def __add__(self, other):
		return FunctionalFunction(compose(other, self))

class ParseRunner:
	def __init__(self, numArgs):
		self.numArgs = numArgs

	def __call__(self, func):
		def wrapped(tks):
			p = 0
			while p < len(tks):# - self.numArgs:
				try:
					r = func(tks, p)
				except IndexError:
					r = None
				if r is not None:
					del tks[p:p+self.numArgs]
					tks.insert(p,r)
				p += 1
			return tks
		return FunctionalFunction(wrapped)

@ParseRunner(3)
def biopParser(tkens, pos):
	if (tkens[pos].tag in EXPRESSION and
		tkens[pos+1].tag==BIOP and
		tkens[pos+2].tag in EXPRESSION):
		#parses expression
		return Token(value=tkens[pos+1].value, tag='BIOPEXP', args=[tkens[pos],tkens[pos+2]])
	else: return None

@ParseRunner(3)
def parenParser(tkens, pos):
	if (tkens[pos].tag==LPAREN and
		tkens[pos+1].tag in EXPRESSION and
		tkens[pos+2].tag==RPAREN):
		#parses expression
		return tkens[pos+1]
	else: return None

@ParseRunner(3)
def asopParser(tkens, pos):
	if (tkens[pos].tag== ID and
		tkens[pos+1].tag==ASOP and
		tkens[pos+2].tag in EXPRESSION):
		#parses expression
		return Token(value=tkens[pos].value, tag='ASOPS', args=tkens[pos+2])
	else: return None

@ParseRunner(2)
def uniopParser(tkens, pos):
	if (tkens[pos].tag==UNIOP and
		tkens[pos+1].tag in EXPRESSION):
		return Token(value=tkens[pos].value, tag='UNIOPEXP', args=tkens[pos+1])
	else: return None

@ParseRunner(2)
def ioStateParser(tkens, pos):
	if (tkens[pos].tag==IOSTATE and 
		(tkens[pos+1].tag==ID or
			(tkens[pos].value[-1]=='<' and tkens[pos+1].tag in EXPRESSION))):
		return Token(value=tkens[pos].value, tag='IOSTATES', args=tkens[pos+1])
	else: return None

runParser = uniopParser + ioStateParser + biopParser + parenParser

def Parse(tokenlist):
	origr = ''
	while origr != repr(tokenlist):
		origr = repr(tokenlist)
		tokenlist = runParser(tokenlist)
	tokenlist = asopParser(tokenlist)
	return tokenlist