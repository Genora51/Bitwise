from basefuncs import *
from functional import compose

class FunctionalFunction(object):
	def __init__(self, func):
		self.func = func
	def __call__(self, *args, **kwargs):
		return self.func(*args, **kwargs)
	def __add__(self, other):
		return FunctionalFunction(compose(other, self))

class ParserError(Exception):
    def __init__(self):
        message = "Parse Error"
        super(ParserError, self).__init__(message)

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
				else:
					p += 1
			return tks
		return FunctionalFunction(wrapped)

def condParser(ts):
	p = 1
	stops = []
	while p <= len(ts):
		if ts[-p].tag == ENDCON:
			stops.append(p)
			#print(ts[-p], p)
		elif ts[-p].tag == CONDSTATE:
			try:
				end = -stops.pop()
			except IndexError:
				raise ParserError
			states = ts[1-p:end]
			if all(t.tag in STATEMENT for t in states[1:]) and states[0].tag in EXPRESSION:
				op = ts[-p].value
				tok = Token(value=op,tag='CONDSTATES',args=states)
				del ts[-p:end+1]
				ts.insert(end+1,tok)
				p = -end
			else:
				raise ParserError
		p += 1
	return ts


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
	tokenlist = condParser(asopParser(tokenlist))
	return tokenlist