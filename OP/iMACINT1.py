

def iMACINT1(V, X, Y):
	"""
	Re-interpret signed integers
	"""
	if V >= 0x80000000:
		V -= 0x100000000
	if X >= 0x80000000:
		X -= 0x100000000
	if Y >= 0x80000000:
		Y -= 0x100000000
	
	"""
	Do the operation
	"""
	Z = V + X * Y
	
	"""
	Wrap-around. Note that this function can *never* output a negative
	number, it is always a number between 0 and 0x7FFFFFFF no matter
	what the inputs are.
	"""
	Z = Z % 0x80000000
	
	return Z

