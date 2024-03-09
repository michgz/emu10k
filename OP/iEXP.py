"""
A bit-exact re-implementation of the operation of the iEXP op-code of the
FX8010 DSP.

    iEXP(V, X, Y)
    
Inputs:
  V    The input (value to take the exponential of). An unsigned integer between 0 and
         4294967295. In the context of FX8010 this number may represent a signed
         value ("may" depending on the value of Y), but in this re-implementation all
         inputs and outputs are unsigned.
  X    Maximum exponent. An unsigned integer between 0 and 4294967295. For users of
         FX8010 it is likely specified that this number should be between 0 and 31
         with other values giving results that are "undefined". This re-implementation
         however matches FX8010 behaviour even with "undefined" inputs.
  Y    Negatives handling. An unsigned integer between 0 and 4294967295. For users of
         FX8010 it is likely specified that this number should be between 0 and 3
         with other values giving results that are "undefined". This re-implementation
         however matches FX8010 behaviour even with "undefined" inputs.
Returns:
  An unsigned integer between 0 and 4294967295. As with X, this is representing a
  signed integer in the context of FX8010.

This has been confirmed bit-exact by comparing against FX8010 with many trial inputs.
"""

def iEXP(V, X, Y):

	X = X % 32     # Just repeats after 31.
	Y = Y % 4      # Just repeats after 3.

	S = 0
	if V >= 0x80000000:
		V = V & 0x7FFFFFFF
		V = V ^ 0x7FFFFFFF
		S = 1
		
	if Y == 2:
		S = 1
	elif Y == 3:
		S = 1-S

	
	if X==1:
		Z = V
	elif X==0:
		Z = 2*V
	
	elif X<4:
		M = V >> 29
		
		if M == 0 or M==1:
			Z =  V>>(X-2)
		else:
			V = V & 0x1FFFFFFF

			if M > (X+1):
				"""
				This code path is impossible; kept here simply for comparison with cases
				below.
				"""
				return 1<<(M-X-2) | (V>>(X+31-M))
			else:
				Z =  (V | 0x20000000)<<(M-X+1)

	elif X<8:
		M = V >> 28
		
		if M==0:
			Z =  V>>(X-3)
		elif M==1:
			Z =  V>>(X-3)
		else:
			V = V & 0x0FFFFFFF
			
			if M > (X+1):
				"""
				An error condition! The iLOG function (of which this is an inverse)
				cannot produce this as output, however it's been verified that this is
				how the FX8010 behaves when given this input.
				"""
				Z = 1<<(M-X-2) | (V>>(X+30-M))
			elif (M-X+2)>=0:
				Z =  (V | 0x10000000)<<(M-X+2)
			else:
				Z =  (V | 0x10000000)>>(-(M-X+2))
				
	elif X<16:
		M = V >> 27
		
		if M==0:
			Z =  V>>(X-4)
		elif M==1:
			Z =  V>>(X-4)
		else:
			V = V & 0x07FFFFFF
			
			if M > (X+1):
				"""
				An error condition! The iLOG function (of which this is an inverse)
				cannot produce this as output, however it's been verified that this is
				how the FX8010 behaves when given this input.
				"""
				return 1<<(M-X-2) | (V>>(X+29-M))
			elif (M-X+3)>=0:
				Z =  (V | 0x08000000)<<(M-X+3)
			else:
				Z =  (V | 0x08000000)>>(-(M-X+3))


	elif X<32:
		M = V >> 26
		
		if M==0:
			Z = V>>(X-5)
		elif M==1:
			Z = V>>(X-5)
		else:
			V = V & 0x07FFFFFF
			
			if M > (X+1):
				"""
				An error condition! The iLOG function (of which this is an inverse)
				cannot produce this as output, however it's been verified that this is
				how the FX8010 behaves when given this input.
				"""
				return 1<<(M-X-2) | (V>>(X+28-M))
			elif (M-X+4)>=0:
				Z = (V | 0x04000000)<<(M-X+4)
			else:
				Z = (V | 0x04000000)>>(-(M-X+4))

	if S == 1:
		if Y == 1:
			return Z
		elif Z >= 0xFFFFFFFC:
			return Z
		else:
			return 0x00000000 | (Z ^ 0xFFFFFFFF)
	else:
		return Z


if __name__=="__main__":
	pass
	# TODO: put some interesting cases here.
