#import statements
from bitwise.lexer import lex
from bitwise.basefuncs import tokens
from bitwise.bitparser import Parse
from bitwise.evaluator import runStates

#load file
with open('add.bit') as f:
	data = f.read()
	f.close()

#Lexes the code
print('LEXED CODE:')
tokns = lex(data, tokens)
for tokenl in tokns:
	print(tokenl)
input('\n----------------\n')

# Parses the lexed code
print('PARSED CODE:')
parsed = Parse(tokns)
for tokenl in parsed:
	print(tokenl)
#Should print parsed code
input('\n----------------\n')
runStates(parsed)