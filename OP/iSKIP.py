
def iSKIP(V, X, Y):
	"""
	Returns True if will skip, False if will not skip.
  Params:
    V: the contents of the GPR_COND register
    X: the condition word
    Y: the number of spaces to skip. Unused in this function, as this simply
        returns True or False for whether or not the skip happens at all
	"""
	
	"""
	V *must* be GPR_COND. The As10k1 Manual says any register can used in
	this position but that appears to be incorrect.
	"""
	
	FORM = ((X >> 30) & 3) + 1
	
	def TEST_BIT(XX,BB):
		return ((XX&(1<<BB))!=0)
	
	if FORM==1:
		
		BRACKET_1 = ((X&0x000003FF)!=0)
		BRACKET_2 = ((X&0x000FFC00)!=0)
		BRACKET_3 = ((X&0x3FF00000)!=0)
		
		if TEST_BIT(X,0) and not TEST_BIT(V,0):
			BRACKET_1 = False
		if TEST_BIT(X,1) and not TEST_BIT(V,1):
			BRACKET_1 = False
		if TEST_BIT(X,2) and not TEST_BIT(V,2):
			BRACKET_1 = False
		if TEST_BIT(X,3) and not TEST_BIT(V,3):
			BRACKET_1 = False
		if TEST_BIT(X,4) and not TEST_BIT(V,4):
			BRACKET_1 = False
		if TEST_BIT(X,5) and TEST_BIT(V,0):
			BRACKET_1 = False
		if TEST_BIT(X,6) and TEST_BIT(V,1):
			BRACKET_1 = False
		if TEST_BIT(X,7) and TEST_BIT(V,2):
			BRACKET_1 = False
		if TEST_BIT(X,8) and TEST_BIT(V,3):
			BRACKET_1 = False
		if TEST_BIT(X,9) and TEST_BIT(V,4):
			BRACKET_1 = False

		if TEST_BIT(X,10) and not TEST_BIT(V,0):
			BRACKET_2 = False
		if TEST_BIT(X,11) and not TEST_BIT(V,1):
			BRACKET_2 = False
		if TEST_BIT(X,12) and not TEST_BIT(V,2):
			BRACKET_2 = False
		if TEST_BIT(X,13) and not TEST_BIT(V,3):
			BRACKET_2 = False
		if TEST_BIT(X,14) and not TEST_BIT(V,4):
			BRACKET_2 = False
		if TEST_BIT(X,15) and TEST_BIT(V,0):
			BRACKET_2 = False
		if TEST_BIT(X,16) and TEST_BIT(V,1):
			BRACKET_2 = False
		if TEST_BIT(X,17) and TEST_BIT(V,2):
			BRACKET_2 = False
		if TEST_BIT(X,18) and TEST_BIT(V,3):
			BRACKET_2 = False
		if TEST_BIT(X,19) and TEST_BIT(V,4):
			BRACKET_2 = False
	
		if TEST_BIT(X,20) and not TEST_BIT(V,0):
			BRACKET_3 = False
		if TEST_BIT(X,21) and not TEST_BIT(V,1):
			BRACKET_3 = False
		if TEST_BIT(X,22) and not TEST_BIT(V,2):
			BRACKET_3 = False
		if TEST_BIT(X,23) and not TEST_BIT(V,3):
			BRACKET_3 = False
		if TEST_BIT(X,24) and not TEST_BIT(V,4):
			BRACKET_3 = False
		if TEST_BIT(X,25) and TEST_BIT(V,0):
			BRACKET_3 = False
		if TEST_BIT(X,26) and TEST_BIT(V,1):
			BRACKET_3 = False
		if TEST_BIT(X,27) and TEST_BIT(V,2):
			BRACKET_3 = False
		if TEST_BIT(X,28) and TEST_BIT(V,3):
			BRACKET_3 = False
		if TEST_BIT(X,29) and TEST_BIT(V,4):
			BRACKET_3 = False
	
		return BRACKET_1 or BRACKET_2 or BRACKET_3
	
	elif FORM==2:
		
		BRACKET_1 = False
		BRACKET_2 = False
		BRACKET_3 = False
		
		if TEST_BIT(X,0) and TEST_BIT(V,0):
			BRACKET_1 = True
		if TEST_BIT(X,1) and TEST_BIT(V,1):
			BRACKET_1 = True
		if TEST_BIT(X,2) and TEST_BIT(V,2):
			BRACKET_1 = True
		if TEST_BIT(X,3) and TEST_BIT(V,3):
			BRACKET_1 = True
		if TEST_BIT(X,4) and TEST_BIT(V,4):
			BRACKET_1 = True
		if TEST_BIT(X,5) and not TEST_BIT(V,0):
			BRACKET_1 = True
		if TEST_BIT(X,6) and not TEST_BIT(V,1):
			BRACKET_1 = True
		if TEST_BIT(X,7) and not TEST_BIT(V,2):
			BRACKET_1 = True
		if TEST_BIT(X,8) and not TEST_BIT(V,3):
			BRACKET_1 = True
		if TEST_BIT(X,9) and not TEST_BIT(V,4):
			BRACKET_1 = True

		if TEST_BIT(X,10) and TEST_BIT(V,0):
			BRACKET_2 = True
		if TEST_BIT(X,11) and TEST_BIT(V,1):
			BRACKET_2 = True
		if TEST_BIT(X,12) and TEST_BIT(V,2):
			BRACKET_2 = True
		if TEST_BIT(X,13) and TEST_BIT(V,3):
			BRACKET_2 = True
		if TEST_BIT(X,14) and TEST_BIT(V,4):
			BRACKET_2 = True
		if TEST_BIT(X,15) and not TEST_BIT(V,0):
			BRACKET_2 = True
		if TEST_BIT(X,16) and not TEST_BIT(V,1):
			BRACKET_2 = True
		if TEST_BIT(X,17) and not TEST_BIT(V,2):
			BRACKET_2 = True
		if TEST_BIT(X,18) and not TEST_BIT(V,3):
			BRACKET_2 = True
		if TEST_BIT(X,19) and not TEST_BIT(V,4):
			BRACKET_2 = True
	
		if TEST_BIT(X,20) and TEST_BIT(V,0):
			BRACKET_3 = True
		if TEST_BIT(X,21) and TEST_BIT(V,1):
			BRACKET_3 = True
		if TEST_BIT(X,22) and TEST_BIT(V,2):
			BRACKET_3 = True
		if TEST_BIT(X,23) and TEST_BIT(V,3):
			BRACKET_3 = True
		if TEST_BIT(X,24) and TEST_BIT(V,4):
			BRACKET_3 = True
		if TEST_BIT(X,25) and not TEST_BIT(V,0):
			BRACKET_3 = True
		if TEST_BIT(X,26) and not TEST_BIT(V,1):
			BRACKET_3 = True
		if TEST_BIT(X,27) and not TEST_BIT(V,2):
			BRACKET_3 = True
		if TEST_BIT(X,28) and not TEST_BIT(V,3):
			BRACKET_3 = True
		if TEST_BIT(X,29) and not TEST_BIT(V,4):
			BRACKET_3 = True
	
		return BRACKET_1 and BRACKET_2 and BRACKET_3
	
	elif FORM==3:
		
		BRACKET_1 = ((X&0x000003FF)!=0)
		BRACKET_2 = ((X&0x000FFC00)!=0)
		BRACKET_3 = False
		
		if TEST_BIT(X,0) and not TEST_BIT(V,0):
			BRACKET_1 = False
		if TEST_BIT(X,1) and not TEST_BIT(V,1):
			BRACKET_1 = False
		if TEST_BIT(X,2) and not TEST_BIT(V,2):
			BRACKET_1 = False
		if TEST_BIT(X,3) and not TEST_BIT(V,3):
			BRACKET_1 = False
		if TEST_BIT(X,4) and not TEST_BIT(V,4):
			BRACKET_1 = False
		if TEST_BIT(X,5) and TEST_BIT(V,0):
			BRACKET_1 = False
		if TEST_BIT(X,6) and TEST_BIT(V,1):
			BRACKET_1 = False
		if TEST_BIT(X,7) and TEST_BIT(V,2):
			BRACKET_1 = False
		if TEST_BIT(X,8) and TEST_BIT(V,3):
			BRACKET_1 = False
		if TEST_BIT(X,9) and TEST_BIT(V,4):
			BRACKET_1 = False

		if TEST_BIT(X,10) and not TEST_BIT(V,0):
			BRACKET_2 = False
		if TEST_BIT(X,11) and not TEST_BIT(V,1):
			BRACKET_2 = False
		if TEST_BIT(X,12) and not TEST_BIT(V,2):
			BRACKET_2 = False
		if TEST_BIT(X,13) and not TEST_BIT(V,3):
			BRACKET_2 = False
		if TEST_BIT(X,14) and not TEST_BIT(V,4):
			BRACKET_2 = False
		if TEST_BIT(X,15) and TEST_BIT(V,0):
			BRACKET_2 = False
		if TEST_BIT(X,16) and TEST_BIT(V,1):
			BRACKET_2 = False
		if TEST_BIT(X,17) and TEST_BIT(V,2):
			BRACKET_2 = False
		if TEST_BIT(X,18) and TEST_BIT(V,3):
			BRACKET_2 = False
		if TEST_BIT(X,19) and TEST_BIT(V,4):
			BRACKET_2 = False
	
		if TEST_BIT(X,20) and TEST_BIT(V,0):
			BRACKET_3 = True
		if TEST_BIT(X,21) and TEST_BIT(V,1):
			BRACKET_3 = True
		if TEST_BIT(X,22) and TEST_BIT(V,2):
			BRACKET_3 = True
		if TEST_BIT(X,23) and TEST_BIT(V,3):
			BRACKET_3 = True
		if TEST_BIT(X,24) and TEST_BIT(V,4):
			BRACKET_3 = True
		if TEST_BIT(X,25) and not TEST_BIT(V,0):
			BRACKET_3 = True
		if TEST_BIT(X,26) and not TEST_BIT(V,1):
			BRACKET_3 = True
		if TEST_BIT(X,27) and not TEST_BIT(V,2):
			BRACKET_3 = True
		if TEST_BIT(X,28) and not TEST_BIT(V,3):
			BRACKET_3 = True
		if TEST_BIT(X,29) and not TEST_BIT(V,4):
			BRACKET_3 = True
	
		return BRACKET_1 or BRACKET_2 or BRACKET_3
	
	elif FORM==4:
		
		BRACKET_1 = False
		BRACKET_2 = False
		BRACKET_3 = ((X&0x3FF00000)!=0)
		
		if TEST_BIT(X,0) and TEST_BIT(V,0):
			BRACKET_1 = True
		if TEST_BIT(X,1) and TEST_BIT(V,1):
			BRACKET_1 = True
		if TEST_BIT(X,2) and TEST_BIT(V,2):
			BRACKET_1 = True
		if TEST_BIT(X,3) and TEST_BIT(V,3):
			BRACKET_1 = True
		if TEST_BIT(X,4) and TEST_BIT(V,4):
			BRACKET_1 = True
		if TEST_BIT(X,5) and not TEST_BIT(V,0):
			BRACKET_1 = True
		if TEST_BIT(X,6) and not TEST_BIT(V,1):
			BRACKET_1 = True
		if TEST_BIT(X,7) and not TEST_BIT(V,2):
			BRACKET_1 = True
		if TEST_BIT(X,8) and not TEST_BIT(V,3):
			BRACKET_1 = True
		if TEST_BIT(X,9) and not TEST_BIT(V,4):
			BRACKET_1 = True

		if TEST_BIT(X,10) and TEST_BIT(V,0):
			BRACKET_2 = True
		if TEST_BIT(X,11) and TEST_BIT(V,1):
			BRACKET_2 = True
		if TEST_BIT(X,12) and TEST_BIT(V,2):
			BRACKET_2 = True
		if TEST_BIT(X,13) and TEST_BIT(V,3):
			BRACKET_2 = True
		if TEST_BIT(X,14) and TEST_BIT(V,4):
			BRACKET_2 = True
		if TEST_BIT(X,15) and not TEST_BIT(V,0):
			BRACKET_2 = True
		if TEST_BIT(X,16) and not TEST_BIT(V,1):
			BRACKET_2 = True
		if TEST_BIT(X,17) and not TEST_BIT(V,2):
			BRACKET_2 = True
		if TEST_BIT(X,18) and not TEST_BIT(V,3):
			BRACKET_2 = True
		if TEST_BIT(X,19) and not TEST_BIT(V,4):
			BRACKET_2 = True
	
		if TEST_BIT(X,20) and not TEST_BIT(V,0):
			BRACKET_3 = False
		if TEST_BIT(X,21) and not TEST_BIT(V,1):
			BRACKET_3 = False
		if TEST_BIT(X,22) and not TEST_BIT(V,2):
			BRACKET_3 = False
		if TEST_BIT(X,23) and not TEST_BIT(V,3):
			BRACKET_3 = False
		if TEST_BIT(X,24) and not TEST_BIT(V,4):
			BRACKET_3 = False
		if TEST_BIT(X,25) and TEST_BIT(V,0):
			BRACKET_3 = False
		if TEST_BIT(X,26) and TEST_BIT(V,1):
			BRACKET_3 = False
		if TEST_BIT(X,27) and TEST_BIT(V,2):
			BRACKET_3 = False
		if TEST_BIT(X,28) and TEST_BIT(V,3):
			BRACKET_3 = False
		if TEST_BIT(X,29) and TEST_BIT(V,4):
			BRACKET_3 = False
	
		return BRACKET_1 and BRACKET_2 and BRACKET_3

	return None

