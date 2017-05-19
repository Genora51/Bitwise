#import statements
from bitwise.lexer import lex
from bitwise.basefuncs import tokens
from bitwise.bitparser import Parse

exp = '!101'

lexed = lex(exp, tokens)
parsed = Parse(lexed)
for token in parsed:
	print(token)