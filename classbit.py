class Bit(object):
	def __init__(self,binst):
		self.st = binst

	def __getitem__(self, index):
		if index >= len(self.st):
			return Bit('0')
		else:
			return Bit(self.st[-1-index])

	def __add__(self, bit):
		ast = self.st + bit.st
		return Bit(ast)

	def __iter__(self):
		return (self[n] for n in range(len(self.st)))

	def __len__(self):
		return len(self.st)

	def __or__(self, bit):
		newst = ''
		ln = max(len(self), len(bit))
		for a in range(ln):
			newst = bin(int(self[a].st,2)|int(bit[a].st,2))[2:] + newst
		return Bit(newst)

	def __repr__(self):
		return ("Bit(%s)"%(repr(self.st)))

	def __and__(self, bit):
		newst = ''
		ln = max(len(self), len(bit))
		for a in range(ln):
			newst = bin(int(self[a].st,2)&int(bit[a].st,2))[2:] + newst
		return Bit(newst)

	def __xor__(self, bit):
		newst = ''
		ln = max(len(self), len(bit))
		for a in range(ln):
			newst =  bin(int(self[a].st,2)^int(bit[a].st,2))[2:] + newst
		return Bit(newst)

	def __rshift__(self, bit):
		newst =  bin(int(self.st,2)>>int(bit.st,2))[2:]
		return Bit(newst)

	def __lshift__(self, bit):
		newst =  bin(int(self.st,2)>>int(bit.st,2))[2:]
		return Bit(newst)

	def __invert__(self):
		newst = ''
		ln = len(self)
		for a in range(ln):
			newst = ('1' if self[a].st == '0' else '0') + newst
		return Bit(newst)

	def hash(self):
		nst = self.st[1:]
		return Bit(nst)
