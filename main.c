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

int main()
{
#if 0
	int f = open("/dev/snd/pcmC1D2p", O_NONBLOCK);
	
	void * buf2  = malloc(sizeof(struct snd_emu10k1_fx8010_code)+10000);
	
	if (buf2 == NULL)
		return -1;
	struct snd_emu10k1_fx8010_code * CODE = (struct snd_emu10k1_fx8010_code *) buf2;
	
	__u32 * BUFF = (__u32 *)(buf2 + sizeof(struct snd_emu10k1_fx8010_code));
	
	memset(CODE, 0, sizeof(struct snd_emu10k1_fx8010_code));
	
	CODE->code = BUFF;
	CODE->code_valid[0] = ~((unsigned long)0);
	
	printf("%d\n", f);
	
	
	//int yy = ioctl(f, (2UL << 30) | (2060UL << 16) | (0x48 << 8) | (0x10UL << 0), buf2);
	//int yy = ioctl(f, (2UL << 30) | (sizeof(int) << 16) | (0x48 << 8) | (0x40UL << 0), buf2);
	//int yy = ioctl(f, (2UL << 30) | (sizeof(int) << 16) | (0x48 << 8) | (0x84UL << 0), buf2);
	int yy = ioctl(f, SNDRV_EMU10K1_IOCTL_CODE_PEEK/*(2UL << 30) | (sizeof(struct snd_emu10k1_fx8010_code) << 16) | (0x48 << 8) | (0x12UL << 0)*/, buf2);
	printf("%d\n", yy);
	printf("%d\n", errno);
	
	
	printf("%d,%d,%d,%d,%d\n", EBADF,EFAULT,EINVAL,ENOTTY,ENOTTY);
	
	
	if (yy >= 0)
	{
		//printf("%08X\n", ((uint32_t*)buf2)[0]);
		//printf("%08X\n", ((uint32_t*)buf2)[1]);
		//printf("%08X\n", ((uint32_t*)buf2)[2]);
		//printf("%08X\n", ((uint32_t*)buf2)[3]);
		//printf("%08X\n", ((uint32_t*)buf2)[4]);
		//printf("%08X\n", ((uint32_t*)buf2)[5]);
		//printf("%08X\n", ((uint32_t*)buf2)[6]);
		//printf("%08X\n", ((uint32_t*)buf2)[7]);
		//printf("%08X\n", ((uint32_t*)buf2)[514]);
		printf("%08X\n", (BUFF[0]));
		printf("%08X\n", (BUFF[1]));
		printf("%08X\n", (BUFF[2]));
		printf("%08X\n", (BUFF[3]));
	}
	
	
	
	free(buf2);
	
	close(f);
	return 0;
	
#endif // 0


#if 0
    void * buf  = malloc(0x800*4);
    if (buf == NULL)
    {
        return -1;
    }

    
    printf("%08X\n", (uint32_t) buf);


    int y = ioperm(0xE000, 32*8, 1);
    printf("%d\r\n", y);
    
    int i;

    for (i = 0x100; i < 0x800; i += 1)
    {
        outl(  (((uint32_t) i) << 16),   0xE000+0x00);
        uint32_t x = inl(0xE000+0x4);
        
        ((uint32_t*) buf)[4*i] = x;
        
    }

    
    usleep(1000);
    
    y = ioperm(0xE000, 32*8, 0);
    printf("%d\r\n", y);

#if 1
    for (i = 0x100; i < 0x800; i += 1)
    {
        if (i % 4 == 0)
        {
            printf("%08X  ", (uint32_t) i);
        }

        printf("%08X ", ((uint32_t*) buf)[4*i]);
        if (i % 4 == 3)
        {
            printf("\n");
        }
    }
    printf("\n");
#endif

    printf("%08X\n", (uint32_t) buf);
    free(buf);

#endif // 0

#if 1

    int y = ioperm(0xE000, 32*8, 1);
    printf("%d\r\n", y);


    outl (((uint32_t) (0x43)) << 16,   0xE000+0x00);
    y = inl  ( 0xE000+0x4 );
    
    printf("Contents of FXWC: %X\r\n", y);

// Overwrite most of the microcode with just copying in noise
int ptr = 0x0;

//while (ptr < 12)
//{
//	OP(NULL, &ptr, iACC3, C_00000000, C_00000000, C_00000000, C_00000000);
//}



ptr = 0x30;
int z;
// These are defined in emufx.c . May have changed?
#define INPUT_CHANNEL_COUNT 12
#define PLAYBACK_CHANNEL_COUNT 8
#define CAPTURE_CHANNEL_COUNT 4
for (z = 0; z < INPUT_CHANNEL_COUNT + PLAYBACK_CHANNEL_COUNT + CAPTURE_CHANNEL_COUNT ; z ++)
{
	//OP(NULL, &ptr, iMACINT0, GPR(z), C_00000000, GPR_NOISE0, C_00000001);
}

for (z = 16; z < 32 ; z ++)
{
//	OP(NULL, &ptr, iMAC0, EXTOUT(z), GPR(z-16), GPR_NOISE0, C_20000000);
	OP(NULL, &ptr, iMACINT0, EXTOUT(z), C_00000000, FXBUS(z-16), C_00000001);
}

//OP(NULL, &ptr, iMAC0, EXTOUT(16), EXTOUT(0), GPR_NOISE0, C_20000000);
//OP(NULL, &ptr, iMAC0, EXTOUT(17), EXTOUT(1), GPR_NOISE0, C_20000000);
//OP(NULL, &ptr, iMAC0, EXTOUT(30), EXTOUT(0), C_00000000, C_20000000);
//OP(NULL, &ptr, iMAC0, EXTOUT(31), EXTOUT(1), C_00000000, C_20000000);




while (ptr < 0x200)
{
	OP(NULL, &ptr, iACC3, C_00000000, C_00000000, C_00000000, C_00000000);
}

   // outl ((uint32_t) (0x43)  << 16,   0xE000+0x00);
   // outl  ( 0x55550000UL,  0xE000+0x4 );



    usleep(1000);
    
    y = ioperm(0xE000, 32*8, 0);
    printf("%d\r\n", y);

#endif



    return 0;
}

