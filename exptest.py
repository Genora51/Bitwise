#import statements
from lexer import lex
from basefuncs import tokens
from bitparser import Parse

exp = '!101'

lexed = lex(exp, tokens)
parsed = Parse(lexed)
for token in parsed:
	print(token)