class Token(object):
	def __init__(self, value, tag, args=None):
		self.value = value
		self.tag = tag
		self.args = args

	def __repr__(self):
		if self.args:
			return ("Token(value=%s,tag=%s,args=%s)" % (repr(self.value), repr(self.tag),repr(self.args)))
		else:
			return ("Token(value=%s,tag=%s)" % (repr(self.value), repr(self.tag)))

import sys
def raiseErr(message, pos=(0,0)):
	raiseErrN(message + " on line %s, position %s." %(pos[0],pos[1]))

def raiseErrN(message):
	sys.stderr.write(message)
	sys.exit(0)

BIOP = 'BIOP'
UNIOP = 'UNIOP'
IOSTATE = 'IOSTATE'
ASOP = 'ASOP'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
CONDSTATE = 'CONDSTATE'
ENDCON = 'ENDCON'
LITERAL = 'LITERAL'
ID = 'ID'
STATEMENT = ['IOSTATES','CONDSTATES','ASOPS']
EXPRESSION = ['ID','LITERAL','UNIOPEXP','BIOPEXP']

tokens = [
	(r"(?m)(^/.*\n)|(/.*)", None),
	(r"\s", None),
	(r"(!?[+^&])|>>|<<|\.|@|_",BIOP),
	(r"[IHS]?[<>]",IOSTATE),
	(r"[!#'$£]", UNIOP),
	(r"[~\-?]", CONDSTATE),
	(r"\;", ENDCON),
	(r"=",ASOP),
	(r"\(", LPAREN),
	(r"\)", RPAREN),
	(r"[01]+", LITERAL),
	(r"([a-zA-Z]+)|\"", ID)
]