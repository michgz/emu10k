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

#define PTR			0x00
#define DATA			0x04

#define FXRT			0x0b		/* Effects send routing register			*/
						/* NOTE: It is illegal to assign the same routing to	*/
						/* two effects sends.					*/
#define FXRT_CHANNELA		0x000f0000	/* Effects send bus number for channel's effects send A	*/
#define FXRT_CHANNELB		0x00f00000	/* Effects send bus number for channel's effects send B	*/
#define FXRT_CHANNELC		0x0f000000	/* Effects send bus number for channel's effects send C	*/
#define FXRT_CHANNELD		0xf0000000	/* Effects send bus number for channel's effects send D	*/

#define SUB_REG(A,B,C)

#define DSL			0x07		/* Send D amount and loop end address register	*/
SUB_REG(DSL, FXSENDAMOUNT_D,	0xff000000)	/* Linear level of channel output sent to FX send bus D	*/
#define PSST			0x06		/* Send C amount and loop start address register	*/
SUB_REG(PSST, FXSENDAMOUNT_C,	0xff000000)	/* Linear level of channel output sent to FX send bus C	*/
#define PTRX			0x01		/* Pitch target and send A/B amounts register		*/
SUB_REG(PTRX, FXSENDAMOUNT_A,	0x0000ff00)	/* Linear level of channel output sent to FX send bus A	*/
SUB_REG(PTRX, FXSENDAMOUNT_B,	0x000000ff)	/* Linear level of channel output sent to FX send bus B	*/

int main()
{
    int y = ioperm(0xE000, 32*8, 1);
    printf("%d\r\n", y);

	uint8_t a1[64];
	uint8_t a2[64];
	uint8_t a3[64];
	uint8_t a4[64];
	uint8_t b1[64];
	uint8_t b2[64];
	uint8_t b3[64];
	uint8_t b4[64];


	int i;
	for (i = 0; i < 64; i ++)
	{
		outl( (FXRT<<16)+i,   0xE000+PTR);
		uint32_t x = inl(0xE000+DATA);
		a1[i] = (uint8_t) ((x >> 16) & 0x0000000FUL);
		a2[i] = (uint8_t) ((x >> 20) & 0x0000000FUL);
		a3[i] = (uint8_t) ((x >> 24) & 0x0000000FUL);
		a4[i] = (uint8_t) ((x >> 28) & 0x0000000FUL);
	}
	for (i = 0; i < 64; i ++)
	{
		outl( (PTRX<<16)+i,   0xE000+PTR);
		uint32_t x = inl(0xE000+DATA);
		b1[i] = (uint8_t) ((x >> 8) & 0x000000FFUL);
		b2[i] = (uint8_t) ((x >> 0) & 0x000000FFUL);
	}
	for (i = 0; i < 64; i ++)
	{
		outl( (PSST<<16)+i,   0xE000+PTR);
		uint32_t x = inl(0xE000+DATA);
		b3[i] = (uint8_t) ((x >> 24) & 0x000000FFUL);
	}
	for (i = 0; i < 64; i ++)
	{
		outl( (DSL<<16)+i,   0xE000+PTR);
		uint32_t x = inl(0xE000+DATA);
		b4[i] = (uint8_t) ((x >> 24) & 0x000000FFUL);
	}

    y = ioperm(0xE000, 32*8, 0);
    printf("%d\r\n", y);


	for (i = 0; i < 64; i ++)
	{
		printf("%03d    ", i);
		printf("%01X ", a1[i]);
		printf("%01X ", a2[i]);
		printf("%01X ", a3[i]);
		printf("%01X    ", a4[i]);
		printf("0x%02X ", b1[i]);
		printf("0x%02X ", b2[i]);
		printf("0x%02X ", b3[i]);
		printf("0x%02X\r\n", b4[i]);
	}



    return 0;
}

