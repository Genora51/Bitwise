#!/usr/bin/env python3

"""Bitwise.

Usage:
  bitwise [-i] PROGRAM
  bitwise --shell
  bitwise -h | --help
  bitwise --version


Options:
  -h --help      Show this screen.
  --version      Show version.
  -i --inputend  Whether to pause at the end.
  -s --shell     Run a Bitwise Shell

"""

from blib.bitparser import Parse
from blib.lexer import lex
from blib.basefuncs import tokens, raiseErrN, Token
import os
import atexit
from os.path import expanduser
import pickle
import readline
from blib.evaluator import runStates as evaluate
import hashlib


def h11(w):
    return hashlib.md5(w.encode()).hexdigest()[:9]


def interpret(text, vals=None):
    lexed = lex(text, tokens)
    parsed = Parse(lexed)
    if vals is None:
        return evaluate(parsed)
    else:
        return evaluate(parsed, vals)


def interpretExp(text, vals=None):
    interpret('<' + text, vals)


def runFile(fileName):
    dirf = os.path.dirname(os.path.realpath(fileName))
    cach = r"%s/__bitcache__/%sc" % (dirf, os.path.basename(fileName))
    mtxt = open(fileName).read()
    if os.path.isfile(cach):
        f = open(cach, 'rb')
        hashed = pickle.load(f)
        if h11(mtxt) == str(hashed):
            parsed = pickle.load(f)
        else:
            parsed = parsNo(mtxt, dirf, cach)
        f.close()
    else:
        parsed = parsNo(mtxt, dirf, cach)
    evaluate(parsed)


def parsNo(mtxt, dirs, cach):
    try:
        os.mkdir(dirs + r"/__bitcache__")
    except OSError:
        pass
    lexed = lex(mtxt, tokens)
    parsed = Parse(lexed)
    with open(cach, 'wb') as f:
        pickle.dump(h11(mtxt), f)
        pickle.dump(parsed, f)
    return parsed


def runCmd(args):
    runFile(args['PROGRAM'])
    if args['--inputend']:
        input('Press enter to continue...')


def save(prev_h_len, histfile):
    new_h_len = readline.get_history_length()
    readline.set_history_length(1000)
    readline.append_history_file(new_h_len - prev_h_len, histfile)


def shell(args):
    home = expanduser("~")
    histfile = os.path.join(os.path.expanduser("~"), ".python_history")
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, histfile)
    ext = False
    vs = None
    print("Bitwise Shell")
    print("-" * 20)
    while not ext:
        inp = input('-> ')
        ext = inp == "exit"
        try:
            if not ext:
                if vs is not None:
                    vs = interpret(inp)
                else:
                    vs = interpret(inp, vs)
        except SystemExit as e:
            if e.args[0].startswith('ParserError: Unused '):
                try:
                    interpretExp(inp, vs)
                except SystemExit as er:
                    print(er.args[0])
            else:
                print(e.args[0])


if __name__ == '__main__':
    try:
        from docopt import docopt
    except ImportError:
        raiseErrN(
            "You need docopt!\n"
            "Install it from http://pypi.python.org/pypi/docopt\n"
            "or run pip install docopt."
        )

    arguments = docopt(__doc__, version='Bitwise 0.0.3')
    if arguments['--shell']:
        shell(arguments)
    else:
        runCmd(arguments)
