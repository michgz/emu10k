

def iMACINT0(V, X, Y):
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
	Saturation
	"""
	if Z > 0x7FFFFFFF:
		Z = 0x7FFFFFFF
	elif Z < -0x80000000:
		Z = -0x80000000
	
	"""
	Return, using a modulus to convert to unsigned
	"""
	return Z % 0x100000000

