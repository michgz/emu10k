#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <sys/io.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

//#include "../linux_build/linux-6.2/include/uapi/sound/emu10k1.h"

#include <stdint.h>

typedef uint32_t u32;

static void snd_emu10k1_write_op(void *icode,
				 unsigned int *ptr,
				 u32 op, u32 r, u32 a, u32 x, u32 y)
{
	//u_int32_t *code;
	//if (snd_BUG_ON(*ptr >= 512))
	//	return;
	//code = icode->code + (*ptr) * 2;
	//set_bit(*ptr, icode->code_valid);
	
	uint32_t code[2];
	
	code[0] = ((x & 0x3ff) << 10) | (y & 0x3ff);
	code[1] = ((op & 0x0f) << 20) | ((r & 0x3ff) << 10) | (a & 0x3ff);


    outl(  (((uint32_t) (0x400 + (*ptr)*2)) << 16),   0xE000+0x00);
    outl  ( code[0],  0xE000+0x4 );
    outl(  (((uint32_t) (0x400 + (*ptr)*2) + 1) << 16),   0xE000+0x00);
    outl  ( code[1],  0xE000+0x4 );

	(*ptr)++;
}

#define OP(icode, ptr, op, r, a, x, y) \
	snd_emu10k1_write_op(icode, ptr, op, r, a, x, y)

#define iMAC0	 0x00	/* R = A + (X * Y >> 31)   ; saturation */
#define iMACINT0 0x04	/* R = A + X * Y	   ; saturation */
#define iACC3	 0x06	/* R = A + X + Y	   ; saturation */

#define C_00000000	0x40
#define C_00000001	0x41
#define C_00000008	0x45
#define C_20000000	0x4c         // >> ends up at +0.25 on audacity plot
#define GPR_NOISE0	0x58		/* noise source */
#define GPR_NOISE1	0x59		/* noise source */

#define GPR(x)    ((x)+0x100)
#define FXBUS(x)    (x)
#define EXTIN(x)	(0x10 + (x))
#define EXTOUT(x)	(0x20 + (x))
#define FXBUS2(x)	(0x30 + (x))

int main()
{
    int y = ioperm(0xE000, 32*8, 1);
    printf("%d\r\n", y);


    outl (((uint32_t) (0x43)) << 16,   0xE000+0x00);
    y = inl  ( 0xE000+0x4 );
    
    printf("Contents of FXWC: %X\r\n", y);

    // Overwrite most of the microcode with just copying from inputs to outputs
    int ptr = 0x0;

    // Setting this to 0x30 skips the portion of microcode dedicated to stopping/
    //  starting TRAM. Is that important? It might relate to the second playback
    //  device, but doesn't seem to affect anything else. This line is optional.
    ptr = 0x30;
    
    int z;
    // These are defined in emufx.c . May have changed?
    #define INPUT_CHANNEL_COUNT 12
    #define PLAYBACK_CHANNEL_COUNT 8
    #define CAPTURE_CHANNEL_COUNT 4
    //for (z = 0; z < INPUT_CHANNEL_COUNT + PLAYBACK_CHANNEL_COUNT + CAPTURE_CHANNEL_COUNT ; z ++)
    //{
    //    OP(NULL, &ptr, iMACINT0, GPR(z), C_00000000, GPR_NOISE0, C_00000001);
    //}



    // Copy from all inputs to all outputs. FXBUS seems to be regarded as inputs,
    //  and FXBUS2 as outputs.
    for (z = 0; z < 16 ; z ++)
    {
        OP(NULL, &ptr, iMACINT0, FXBUS2(z), C_00000000, FXBUS(z), C_00000001);
    }


    // Fill the remainder of microcode with no-operations
    while (ptr < 0x200)
    {
        OP(NULL, &ptr, iACC3, C_00000000, C_00000000, C_00000000, C_00000000);
    }


    usleep(1000);
    
    y = ioperm(0xE000, 32*8, 0);
    printf("%d\r\n", y);



    return 0;
}
