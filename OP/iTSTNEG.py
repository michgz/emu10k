

def iTSTNEG(V,X,Y):
	global GPR_COND
	
	"""
	Re-interpret signed integers. Don't need to for X because it
  is treated as binary by this function.
	"""
	if V >= 0x80000000:
		V -= 0x100000000
	if Y >= 0x80000000:
		Y -= 0x100000000
	
	if V>=Y:
		NORM_FLAG = False
		Z = X
	else:
		NORM_FLAG = True
		Z = 0xFFFFFFFF^X
	
	GPR_COND = (0x08 if Z==0 else 0)       \
			 + (0x04 if Z>=0x80000000 else 0)  \
			 + (0x02 if NORM_FLAG else 0)
	
	return Z
