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
#define WC			0x10

#define CCCA			0x08
#define FXBA			0x47
#define MICBS			0x49
#define ADCBS			0x4a
#define FXBS			0x4b
#define MICIDX			0x63
#define ADCIDX			0x64
#define FXIDX			0x65

/*
 * Investigation into the EMU10K1 registers. The 64 channel registers (CCCA
 * and nearby) are to do with playback. The 16 channel FXBS/FXIDX registers
 * are to do with record.
 * */

int main()
{
    int y = ioperm(0xE000, 32*8, 1);
    printf("%d\r\n", y);

    uint32_t a1 = inl(0xE000+WC);
    usleep(1000);
    uint32_t a2 = inl(0xE000+WC);

    printf("0x%08X 0x%08X\r\n", a1, a2);
    
    usleep(1000);
    
    uint32_t b1[64];
    uint32_t b2[64];
    
    int i;
    
    for (i = 0; i < 64; i ++)
    {
        outl((FXIDX<<16) + i, 0xE000+PTR);
        b1[i] = inl(0xE000+DATA);
    }
    usleep(1000);
    for (i = 0; i < 64; i ++)
    {
        outl((FXIDX<<16) + i, 0xE000+PTR);
        b2[i] = inl(0xE000+DATA);
    }
    
    uint32_t c1[6];
    uint32_t c2[6];
    
    outl((MICBS<<16), 0xE000+PTR);
    c1[0] = inl(0xE000+DATA);
    outl((ADCBS<<16), 0xE000+PTR);
    c1[1] = inl(0xE000+DATA);
    outl((FXBS<<16), 0xE000+PTR);
    c1[2] = inl(0xE000+DATA);
    outl((MICIDX<<16), 0xE000+PTR);
    c1[3] = inl(0xE000+DATA);
    outl((ADCIDX<<16), 0xE000+PTR);
    c1[4] = inl(0xE000+DATA);
    outl((FXIDX<<16), 0xE000+PTR);
    c1[5] = inl(0xE000+DATA);
    
    usleep(1000);
    
    outl((MICBS<<16), 0xE000+PTR);
    c2[0] = inl(0xE000+DATA);
    outl((ADCBS<<16), 0xE000+PTR);
    c2[1] = inl(0xE000+DATA);
    outl((FXBS<<16), 0xE000+PTR);
    c2[2] = inl(0xE000+DATA);
    outl((MICIDX<<16), 0xE000+PTR);
    c2[3] = inl(0xE000+DATA);
    outl((ADCIDX<<16), 0xE000+PTR);
    c2[4] = inl(0xE000+DATA);
    outl((FXIDX<<16), 0xE000+PTR);
    c2[5] = inl(0xE000+DATA);

   
    y = ioperm(0xE000, 32*8, 0);
    printf("%d\r\n", y);

    /*for(i = 0; i < 64; i ++)
    {
         printf("%08X  ", b1[i]);
    }
    printf("\r\n");
    for(i = 0; i < 64; i ++)
    {
         printf("%08X  ", b2[i]);
    }
    printf("\r\n");
    
    for(i = 0; i < 64; i ++)
    {
        if (b1[i]!=0 || b2[i]!=0)
        {
            printf("%02d:  %d\r\n", i, b2[i] - b1[i]);
        }
    }
    * */


    for(i = 0 ; i < 6; i ++)
    {
		printf("%08X  ", c1[i]);
	}
	printf("\r\n");
    for(i = 0 ; i < 6; i ++)
    {
		printf("%08X  ", c2[i]);
	}
	printf("    (Increment: %d)", c2[5]-c1[5]);
	printf("\r\n");


    return 0;
}

