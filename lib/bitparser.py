from .basefuncs import *
try:
	from functional import compose
except ImportError:
	raiseErrN("You need functional!\nInstall it from http://pypi.python.org/pypi/functional\nor run pip install functional.")

def ParserError(message, token):
	#print(token)
	raiseErr("ParserError: %s '%s'" %(message, token.value), token.args)

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
		@FunctionalFunction
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
		return wrapped

@FunctionalFunction
def condParser(ts):
	p = 1
	stops = []
	toks = []
	while p <= len(ts):
		tok = ts[-p]
		if tok.tag == ENDCON:
			stops.append(p)
			toks.append(tok)
			#print(ts[-p], p)
		elif tok.tag == CONDSTATE:
			try:
				end = -stops.pop()
				toks.pop()
			except IndexError:
				ParserError("Unmatched Conditional",ts[-p])
			states = ts[1-p:end]
			if all(t.tag in STATEMENT for t in states[1:]) and states[0].tag in EXPRESSION:
				op = ts[-p].value
				tok = Token(value=op,tag='CONDSTATES',args=states)
				del ts[-p:end+1]
				ts.insert(end+1,tok)
				p = -end
			else:
				ParserError("Non-statement in the conditional starting", tok)
		p += 1
	if stops != []:
		ParserError("Unmatched Token", toks.pop())
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

@ParseRunner(2):
def iStateParser(tkens, pos):
	if (tkens[pos].tag==IOSTATE and
		tkens[pos].value[-1]=='>' and
		tkens[pos+1].tag==ID):
		return Token(value=tkens[pos].value, tag='IOSTATES', args=tkens[pos+1])
	else: return None

@ParseRunner(2)
def oStateParser(tkens, pos):
	if (tkens[pos].tag==IOSTATE and
		tkens[pos].value[-1]=='<' and
		tkens[pos+1].tag in EXPRESSION):
		return Token(value=tkens[pos].value, tag='IOSTATES', args=tkens[pos+1])
	else: return None

runParser = uniopParser + iStateParser + biopParser + parenParser
stateParse = oStateParser + asopParser + condParser

def Parse(tokenlist):
	origr = ''
	while origr != repr(tokenlist):
		origr = repr(tokenlist)
		tokenlist = runParser(tokenlist)
	tokenlist = stateParse(tokenlist)
	tst = [a for a in tokenlist if a.tag in (LPAREN, RPAREN)]
	if tst != []:
		ParserError("Unmatched Parenthesis", tst[0])
	tst = [a for a in tokenlist if a.tag not in STATEMENT + ["CONDSTATE", "ENDCON"]]
	if tst != []:
		if tst[0].tag.endswith("EXP"):
			raiseErrN("ParserError: Unused Expression with Operation '%s'"%(tst[0].value))
		else:
			ParserError("Unused Token",tst[0])
	return tokenlist
