# -*- coding: utf-8 -*-
from .basefuncs import *
from .classbit import Bit

biops = {
    '+': lambda a, b: a | b,
    '&': lambda a, b: a & b,
    '^': lambda a, b: a ^ b,
    '.': lambda a, b: a + b,
    '>>': lambda a, b: a >> b,
    '<<': lambda a, b: a << b,
    '!+': lambda a, b: ~(a | b),
    '!&': lambda a, b: ~(a & b),
    '!^': lambda a, b: ~(a ^ b),
    '@': lambda a, b: a[int(b)],
    '_': lambda a, b: a.mxl(b)
}

uniops = {
    '!': lambda x: ~x,
    '#': lambda x: x.hash(),
    '$': lambda x: x[0],
    '£': lambda x: x[-1]
}

inputs = {
    'I>': 'Integer',
    'S>': 'String',
    'H>': 'Hex',
    '>': 'Binary'
}
inputf = {
    'I>': lambda x: bin(int(x))[2:],
    'S>': lambda st: ''.join(format(ord(x), 'b').zfill(8) for x in st),
    'H>': lambda x: bin(int(x, 16))[2:],
    '>': lambda x: x
}
outputf = {
    'I<': int,
    'S<': lambda bits: int(bits).to_bytes((int(bits).bit_length() + 7) // 8, 'big').decode(),
    'H<': lambda x: hex(int(x))[2:],
    '<': lambda x: x.st
}


class vl(dict):
    def __getitem__(self, index):
        try:
            return dict.__getitem__(self, index)
        except KeyError:
            raiseErrN(
                'ReferenceError: Variable \'%s\' referenced before assignment.' % (index))


def litEval(t):
    return Bit(t.value)


def idEval(t, varis):
    # print(t, varis)
    return varis[t.value]


def expEval(t, varlist):
    if t.tag == ID:
        return idEval(t, varlist)
    elif t.tag == LITERAL:
        return litEval(t)
    elif t.tag == 'BIOPEXP':
        t0 = expEval(t.args[0], varlist)
        t1 = expEval(t.args[1], varlist)
        return biops[t.value](t0, t1)
    elif t.tag == 'UNIOPEXP':
        arg = expEval(t.args, varlist)
        if t.value == "'":
            return arg[int(varlist['"'])]
        else:
            return uniops[t.value](arg)


def stateRun(s, varlist):
    # print(s)
    if s.tag == 'ASOPS':
        varlist[s.value] = expEval(s.args, varlist)
    elif s.tag == 'IOSTATES':
        v = s.value
        if v[-1] == '>':
            a = inputf[v](input(inputs[v] + ': '))
            varlist[s.args.value] = Bit(a)
        else:
            print(outputf[v](expEval(s.args, varlist)))
    else:
        doCond(s, varlist)


def doCond(st, varl):
    # print(st)
    toch = expEval(st.args[0], varl)
    if st.value == '-':
        for q in range(len(toch)):
            varl['"'] = Bit(bin(q)[2:])
            runStates(st.args[1:], varl)
    elif st.value == '?':
        if int(toch):
            runStates(st.args[1:], varl)
    else:
        for p in range(len(toch)):
            varl['"'] = Bit(bin(len(toch) - p - 1)[2:])
            runStates(st.args[1:], varl)


def runStates(tls, varls=vl()):
    for t in tls:
        stateRun(t, varls)
    return varls
