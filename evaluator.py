from basefuncs import *
from classbit import Bit

biops = {
	'+': lambda a,b: a|b,
	'&': lambda a,b: a&b,
	'^': lambda a,b: a^b,
	'.': lambda a,b: a+b,
	'>>': lambda a,b: a>>b,
	'<<': lambda a,b: a<<b,
	'!+': lambda a,b: ~(a|b),
	'!&': lambda a,b: ~(a&b),
	'!^': lambda a,b: ~(a^b),
	'@': lambda a,b: a[int(b)]
}

uniops = {
	'!': lambda x: ~x,
	'#': lambda x: x.hash()
	'$': lambda x: x[0]
	'£': lambda x: x[-1]
}

inputs = {
	'I<' : 'Integer',
	'S<' : 'String',
	'H<' : 'Hex',
	'<' : 'Binary'
}

class vl(dict):
	def __getitem__(self, index):
		try:
			return dict.__getitem__(self, index)
		except IndexError:
			raiseErrN('ReferenceError: Variable \'%s\' referenced before assignment.'%(index))

def litEval(t):
	return Bit(t.value)

def idEval(t, varis):
	return varis[t.value]

def expEval(t, varlist):
	if t.tag == ID:
		return idEval(t,varlist)
	elif t.tag == LITERAL:
		return litEval(t)
	elif t.tag == 'BIOPEXP':
		t0 = expEval(t.args[0])
		t1 = expEval(t.args[1])
		return biops[t.value](t0,t1)
	elif t.tag == 'UNIOPEXP':
		arg = expEval(t.args)
		if t.value == "'":
			return arg[int(varlist['"'])]
		else:
			return uniops[t.value](arg)

def stateRun(s, varlist):
	if s.tag == 'ASOPS':
		varlist[s.value] = expEval(s.args)
	elif s.tag == 'IOSTATE':
		v = s.value
		if v[-1] == '<':
			varlist[s.args.value] = input(inputs[v] + ': ')
		else:
			print(expEval(s.args))
	else:
		doCond(s, varlist)

def doCond(st, varl):
	pass