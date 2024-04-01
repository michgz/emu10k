

def iMAC3(V, X, Y):
	global GPR_COND
	
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
	Z = (-(X * Y) >> 31)
	if Z>0x7FFFFFFF or Z<0:
		NORM_FLAG = (  ((V+Z)>0x7FFFFFFF or (V+Z)<0) != (V>0x7FFFFFFF or V<0) )
	else:
		NORM_FLAG = (  ((V+Z)>0x7FFFFFFF or (V+Z)<0) == (V>0x7FFFFFFF or V<0) )
	Z = V + Z
	
	"""
	Wrap-around.
	"""
	SAT_FLAG = (Z > 0x7FFFFFFF) or (Z < -0x7FFFFFFF)
	BORROW_FLAG = (Z > 0x3FFFFFFF) or (Z < -0x3FFFFFFF)
	Z = Z % 0x100000000
	
	"""
	Update the condition register (implemented here as a global variable)
	"""
	GPR_COND = (0x08 if Z==0 else 0)           \
			 + (0x04 if Z>=0x80000000 else 0)  \
			 + (0x10 if SAT_FLAG else 0)       \
			 + (0x01 if BORROW_FLAG else 0)    \
			 + (0x02 if NORM_FLAG else 0)
	
	"""
	Return. No modulus needed, it has been incorporated by the wrap-around
	"""
	return Z

