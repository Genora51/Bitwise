#import statements
from lexer import lex
from basefuncs import tokens
from bitparser import Parse

#load file
with open('add.bit') as f:
	data = f.read()
	f.close()

#Lexes the code
print('LEXED CODE:')
tokns = lex(data, tokens)
for tokenl in tokns:
	print(tokenl)
input('----------------')

# Parses the lexed code
print('PARSED CODE:')
parsed = Parse(tokns)
for tokenl in parsed:
	print(tokenl)
input()
#Should print parsed code
