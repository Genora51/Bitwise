import re
from .basefuncs import *


def LexerError(pos, char):
    message = "Illegal character '%s'" % (char)
    raiseErr(message, pos)


def lex(characters, token_exprs):
    pos = 0
    lpos = [1, 0]
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
                    token = Token(text, tag, args=lpos[:])
                    tokens.append(token)
                break
        if not match:
            LexerError(lpos, characters[pos])
        else:
            # print([text])
            posn = match.end(0)
            lpos[1] += len(text)
            nc = text.count('\n')
            lpos[0] += nc
            if nc > 0:
                lpos[1] = len(text) - text.rfind('\n')
            # print(lpos)
            pos = posn
    return tokens
