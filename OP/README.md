# OP

Bit-exact re-implementations of some the FX8010 op-codes. These have been tested against 1000's
of possible inputs to ensure they give the correct outputs. They are written in simple Python
and so can be studied, or used in emulators as required.

All inputs and outputs here are unsigned 32-bit integers. Many of the op-codes act on values
as signed integers (or, in some cases, even floating-point values). However, to avoid
confusion as to when or if they are to be treated that way, here the inputs and
outputs are just the raw unsigned values and the issue of how to interpret them
are included in the re-implementation.

## iLOG

Not really a logarithm but actually a fixed point-to-floating point conversion with
arbitrarily selectable exponent. A larger exponent moves more of the "information"
in the value into the exponent portion (so, is closer to a true base-2 logarithm)
but risks losing more precision from the mantissa. A value of 7 is commonly used
and is probably a good compromise.

## iEXP

The reverse of iLOG, not really an exponential but a conversion from floating point back to fixed point.
