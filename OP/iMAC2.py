

def iMAC2(V, X, Y):
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
	Z = V + ((X * Y) >> 31)
	
	"""
	Wrap-around.
	"""
	Z = Z % 0x100000000
	
	"""
	Return. No modulus needed, it has been incorporated by the wrap-around
	"""
	return Z

