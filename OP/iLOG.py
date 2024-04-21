"""
A bit-exact re-implementation of the operation of the iLOG op-code of the
FX8010 DSP.

    iLOG(V, X, Y)
    
Inputs:
  V    The input (value to take the logarithm of). An unsigned integer between 0 and
         4294967295. In the context of FX8010 this number is representing a signed
         value, but in this re-implementation all inputs and outputs are unsigned.
  X    Maximum exponent. An unsigned integer between 0 and 4294967295. For users of
         FX8010 it is likely specified that this number should be between 0 and 31
         with other values giving results that are "undefined". This re-implementation
         however matches FX8010 behaviour even with "undefined" inputs.
  Y    Negatives handling. An unsigned integer between 0 and 4294967295. For users of
         FX8010 it is likely specified that this number should be between 0 and 3
         with other values giving results that are "undefined". This re-implementation
         however matches FX8010 behaviour even with "undefined" inputs.
Returns:
  An unsigned integer between 0 and 4294967295. As with X, this may be representing
  a signed integer in the context of FX8010.

This has been confirmed bit-exact by comparing against FX8010 with many trial inputs.
"""

import math

def iLOG(V, X, Y):

	X = X % 32     # Just repeats after 31.
	Y = Y % 4      # Just repeats after 3.

	Z = 0
	S = 0
	if V >= 0x80000000:
		V = (V & 0x7FFFFFFF) ^ 0x7FFFFFFF
		if Y == 0 or Y == 2:
			S = 1
	else:
		if Y == 2 or Y == 3:
			S = 1

	if V == 0:
		Z = 0

	elif X >= 16:
		
		M = math.log2(V)
		if M <= (32-X):
			Z = V << (X-5)
		else:
			P = int(M) - (30-X)
			if P >= (X-4):
				"""
				This code path is impossible; kept here simply for comparison with cases
				below.
				"""
				Q = (V >> (P-(X-4))) - 0x04000000
			else:
				Q = (V << ((X-4)-P)) - 0x04000000

			Z = 0x04000000*P + Q

	elif X >= 8:
		
		M = math.log2(V)
		if M <= (32-X):
			Z = V << (X-4)
		else:
			P = int(M) - (30-X)
			if P >= (X-3):
				Q = (V >> (P-(X-3))) - 0x08000000
			else:
				Q = (V << ((X-3)-P)) - 0x08000000

			Z = 0x08000000*P + Q
		
	elif X >= 4:

		M = math.log2(V)
		if M <= (32-X):
			Z = V << (X-3)
		else:
			P = int(M) - (30-X)
			if P >= (X-2):
				Q = (V >> (P-(X-2))) - 0x10000000
			else:
				Q = (V << ((X-2)-P)) - 0x10000000
			Z = 0x10000000*P + Q

	elif X >= 2:

		M = math.log2(V)
		if M <= (32-X):
			Z = V << (X-2)
		else:
			P = int(M) - (30-X)
			if P >= (X-1):
				Q = (V >> (P-(X-1))) - 0x20000000
			else:
				Q = (V >> ((X-1)-P)) - 0x20000000
			Z = 0x20000000*P + Q
			
		
	elif X == 1:

		Z = V   # This is purely linear

	elif X == 0:
		
		Z = V//2  # Also linear
		
	if S != 0:
		Z = (Z ^ 0x7FFFFFFF) + 0x80000000
	return Z



if __name__=="__main__":
	pass
	# TODO: put some interesting cases here.
