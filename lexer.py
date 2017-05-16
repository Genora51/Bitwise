import sys
import re
from basefuncs import *

class LexerError(Exception):
    def __init__(self, pos, char):
        message = "Illegal character on line %i, column %i: '%s'" %(pos[0],pos[1],char)
        super(LexerError, self).__init__(message)

def lex(characters, token_exprs):
    pos = 0
    lpos = [1,0]
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = Token(text, tag)
                    tokens.append(token)
                break
        if not match:
            raise LexerError(lpos, characters[pos])
        else:
            #print([text])
            posn = match.end(0)
            lpos[1] += len(text)
            nc = text.count('\n')
            lpos[0] += nc
            if nc > 0:
                lpos[1] = len(text) - text.rfind('\n')
            #print(lpos)
            pos = posn
    return tokens