/*
 * Set up the AC'97 to accept data on a particular slot, and then run a
 * test to make sure the EMU10K1 is sending to that slot.
 * 
 * This is of particular significance for STAC9708-based cards (such as 
 * Live! 5.1) where the center & LFE channels are on a secondary AC'97
 * slot.
 * 
 */
 
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

#define C_00000000	0x40
#define C_00000001	0x41
#define C_10000000	0x4b
#define C_20000000	0x4c
#define C_40000000	0x4d
#define C_10000000	0x4b
#define C_00080000	0x4a

#define OP(icode, ptr, op, r, a, x, y) \
	snd_emu10k1_write_op(icode, ptr, op, r, a, x, y)

#define iMAC0	 0x00	/* R = A + (X * Y >> 31)   ; saturation */
#define iMACINT0 0x04	/* R = A + X * Y	   ; saturation */
#define iACC3	 0x06	/* R = A + X + Y	   ; saturation */

#define GPR(x)    ((x)+0x100)
#define FXBUS(x)    (x)
#define EXTIN(x)	(0x10 + (x))
#define EXTOUT(x)	(0x20 + (x))
#define FXBUS2(x)	(0x30 + (x))
#define GPR_NOISE0	0x58		/* noise source */
#define GPR_NOISE1	0x59		/* noise source */

#define PTR			0x00
#define DATA			0x04

#define AC97DATA		0x1c		/* AC97 register set data register (16 bit)	*/

#define AC97ADDRESS		0x1e		/* AC97 register set address register (8 bit)	*/
#define AC97ADDRESS_READY	0x80		/* Read-only bit, reflects CODEC READY signal	*/
#define AC97ADDRESS_ADDRESS	0x7f		/* Address of indexed AC97 register		*/


#define EXTOUT_AC97_L	   0x00	/* AC'97 playback channel - left */
#define EXTOUT_AC97_R	   0x01	/* AC'97 playback channel - right */
#define EXTOUT_ADC_CAP_L   0x0a	/* ADC Capture buffer - left */
#define EXTOUT_ADC_CAP_R   0x0b	/* ADC Capture buffer - right */
#define EXTOUT_AC97_REAR_L 0x0d	/* SB Live 5.1 (c) 2003 - Rear Left */
#define EXTOUT_AC97_REAR_R 0x0e	/* SB Live 5.1 (c) 2003 - Rear Right */
#define EXTOUT_ACENTER	   0x11 /* Analog Center */
#define EXTOUT_ALFE	   0x12 /* Analog LFE */

#define EXTIN_AC97_L	   0x00	/* AC'97 capture channel - left */
#define EXTIN_AC97_R	   0x01	/* AC'97 capture channel - right */

// are these two reversed in the header file???
#define AC97SLOT_REAR_RIGHT	0x01		/* Rear left					*/
#define AC97SLOT_REAR_LEFT	0x02		/* Rear right					*/


// Definitions from linux/include/sound/ac97_codec.h
#define AC97_SIGMATEL_MULTICHN	0x74	/* Multi-Channel programming */



typedef struct AC97_REG
{
	uint8_t addr;
	uint16_t val;
} AC97_REG_T;



#define PTRX			0x01
#define PSST			0x06
#define DSL			0x07
#define FXRT			0x0b
#define AC97SLOT		0x5f

/*
 * AC'97 registers to give a reasonable loop-back behaviour
 * 
 * */
AC97_REG_T REGS [] = {
	{0x02, 0x1616},    // unmute master -- so can hear in analogue output
	{0x04, 0x8808},
	{0x06, 0x8000},
	{0x0A, 0x8000},
	{0x0C, 0x8000},
	{0x0E, 0x8000},
	{0x10, 0x8000},
	{0x12, 0x8000},
	{0x14, 0x8000},
	{0x16, 0x8000},
                      // 0x18 is dealt with specially
	{0x1A, 0x0505},
	{0x1C, 0x0303},
	{0x20, 0x0000},   // no 3D - no need to set 0x22
	{0x22, 0x0000},
	{0x6C, 0x0000}

};



//const int SEL = 4;   // Takes values 0-7.

const int REDUCE_VOL_METHOD = 1;   // Takes values 0-2. Affects SEL=5,6 which
                                   // have a different volume level from the
                                   // other channels for some reason.
                                   //   0 = do nothing with these channels. (Will overload!!)
                                   //   1 = reduce volume digitally (within EMU10k1). This is currently commented out
                                   //   2 = reduce volume in analogue (within AC'97)


int main(int argc, void * argv[])
{
	
	printf("%d \r\n", argc);
	
	
	int SEL = 0;
	uint8_t PCM_Vol = 4;
	
	

	/* First command-line argument is which slot to use (an
	 * index value in range 0-7   */
	if (argc >= 2)
	{
		SEL = atoi(argv[1]);
	}

	/* Second command-line argument is the volume to apply to both
	 * PCM OUT channels (i.e. the DAC)    */
	if (argc >= 3)
	{
		PCM_Vol = atoi(argv[2]);
		printf("%d %d\r\n", SEL, PCM_Vol);
	}
	
    int y = ioperm(0xE000, 32*8, 1);
    printf("%d\r\n", y);

	outl(0x28, 0xE000+AC97ADDRESS);
	usleep(2);
	uint32_t x2 = inw(0xE000+AC97ADDRESS);
	uint32_t x1 = inw(0xE000+AC97DATA);
	printf("%08X %08X\r\n", x1, x2);

	int i;
	for (i = 0; i < sizeof(REGS)/sizeof(REGS[0]); i ++)
	{
		printf("%02X %04X\r\n", REGS[i].addr, REGS[i].val);
		outl(REGS[i].addr, 0xE000+AC97ADDRESS);
		usleep(2);
		outw(REGS[i].val, 0xE000+AC97DATA);
	}
	
	uint8_t Reg74_Val = 0x00;
	switch(SEL)
	{
		case 0:
		case 1:
		default:
			Reg74_Val = 0;
			break;
		case 2:
		case 3:
			Reg74_Val = 2;
			break;
		case 4:
		case 5:
			Reg74_Val = 1;
			break;
		case 6:
		case 7:
			Reg74_Val = 3;
			break;
			
	}


	outl(0x74, 0xE000+AC97ADDRESS);  //AC97_SIGMATEL_MULTICHN
	usleep(2);
	outw((uint16_t)Reg74_Val, 0xE000+AC97DATA);


	//uint8_t PCM_Vol = 4;
	//if ((SEL==5 || SEL==6) && (REDUCE_VOL_METHOD==1))
	//{
	//	// Reduce the volume of these two channels.
	//	PCM_Vol = 7;   // larger = quieter
	//}

	outl(0x18, 0xE000+AC97ADDRESS);
	usleep(2);
	outw((uint16_t)PCM_Vol * 0x0001 + 0x8A00, 0xE000+AC97DATA);

	uint32_t ac97_slot_sel = 0x0;

	switch(SEL)
	{
		case 0:
		case 1:
		default:
			ac97_slot_sel = 0x00;
			break;
		case 2:
			ac97_slot_sel = 0x03;   // neither 1 nor 2 works
			break;
		case 3:
			ac97_slot_sel = 0x02;
			break;
		case 4:
		case 5:
			ac97_slot_sel = 0x30;    // neither 0x10 not 0x20 works
			break;
		case 6:
		case 7:
			ac97_slot_sel = 0x0C;
			break;
			
	}



	outl((AC97SLOT<<16)+0, 0xE000+PTR);
	outl((uint32_t)ac97_slot_sel, 0xE000+DATA);      // Enable the EMU10K1 to output on Read L&R channels, if needed




	int ptr = 0x0;


		
		
	uint8_t ext_out = 0;
	
	switch(SEL)
	{
		case 0:
		default:
			ext_out = EXTOUT_AC97_L;
			break;
		case 1:
			ext_out = EXTOUT_AC97_R;
			break;
		case 2:
			ext_out = EXTOUT_AC97_REAR_L;
			break;
		case 3:
			ext_out = EXTOUT_AC97_REAR_R;
			break;
		case 4:
			ext_out = EXTOUT_ACENTER;
			break;
		case 5:
			ext_out = EXTOUT_ALFE;
			break;
		case 6:
			ext_out = 15;   // a value that's not defined in the uapi_sound_emu10k1.h header!
			break;
		case 7:
			ext_out = 16;   // a value that's not defined in the uapi_sound_emu10k1.h header!
			break;
	}
	
	//Forward playback to the correct channel 
	if ((SEL==5 || SEL==6) && (REDUCE_VOL_METHOD == 2))
	{
		// These channels for some reason needs to be reduced by -12dB, otherwise
		// it will overload
		OP(NULL, &ptr, iMAC0, EXTOUT(ext_out), C_00000000, FXBUS(0), C_20000000);
	}
	else
	{
		OP(NULL, &ptr, iMACINT0, EXTOUT(ext_out), C_00000000, FXBUS(0), C_00000001);
	}


	//Make sure nothing is going to the front channel pair
	if (ext_out != 0)
	{
		OP(NULL, &ptr, iACC3, EXTOUT(0), C_00000000, C_00000000, C_00000000);
	}
	if (ext_out != 1)
	{
		OP(NULL, &ptr, iACC3, EXTOUT(1), C_00000000, C_00000000, C_00000000);
	}


	//Forward AC97 capture to the ADC device
	OP(NULL, &ptr, iMACINT0, EXTOUT(EXTOUT_ADC_CAP_L), C_00000000, EXTIN(EXTIN_AC97_L), C_00000001);
	OP(NULL, &ptr, iMACINT0, EXTOUT(EXTOUT_ADC_CAP_R), C_00000000, EXTIN(EXTIN_AC97_R), C_00000001);


	while (ptr < 0x200)
	{
		OP(NULL, &ptr, iACC3, C_00000000, C_00000000, C_00000000, C_00000000);
	}




    usleep(1000);
    
    y = ioperm(0xE000, 32*8, 0);
    printf("%d\r\n", y);


    return 0;
}

