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
import __init__

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

	BORROW_FLAG = 0


	if V == 0:
		Z = 0

	else:

		M = math.floor(math.log2(V))
		
		# Deal with the Borrow flag
		if M >= (31-X):
			BORROW_FLAG=1

		if M < (32-X):
			if X >= 16:
				Z = V << (X-5)
			elif X >= 8:
				Z = V << (X-4)
			elif X >= 4:
				Z = V << (X-3)
			elif X >= 2:
				Z = V << (X-2)
			elif X == 1:
				Z = V << (X-1)
			elif X == 0:
				Z = V >> 1
		else:

			P = M - (30-X)

			if X >= 16:

				if M >= 26:
					"""
					This code path is impossible; kept here simply for comparison with cases
					below.
					"""
					Q = (V >> (M-26)) - 0x04000000
				else:
					Q = (V << (26-M)) - 0x04000000

				Z = 0x04000000*P + Q

			elif X >= 8:

				if M >= 27:
					Q = (V >> (M-27)) - 0x08000000
				else:
					Q = (V << (27-M)) - 0x08000000

				Z = 0x08000000*P + Q
			
			elif X >= 4:

				if M >= 28:
					Q = (V >> (M-28)) - 0x10000000
				else:
					Q = (V << (28-M)) - 0x10000000
				Z = 0x10000000*P + Q

			elif X >= 2:

				if M >= 29:
					Q = (V >> (M-29)) - 0x20000000
				else:
					Q = (V >> (29-M)) - 0x20000000
				Z = 0x20000000*P + Q

			else:
				"""
				X = 0 or 1 case. Impossible to get here
				"""
				raise Exception


	if S != 0:
		Z = (Z ^ 0x7FFFFFFF) + 0x80000000

	SAT_FLAG = 0
	NORM_FLAG = 1

	"""
	Update the condition register (implemented here as a global variable)
	"""
	__init__.GPR_COND = (0x08 if Z==0 else 0)           \
					  + (0x04 if Z>=0x80000000 else 0)  \
					  + (0x10 if SAT_FLAG else 0)       \
					  + (0x01 if BORROW_FLAG else 0)    \
					  + (0x02 if NORM_FLAG else 0)

	return Z



if __name__=="__main__":
	pass
	# TODO: put some interesting cases here.
