//  https://burgers.io/pci-access-without-a-driver

/*

lspci -d 1102:0002 -nvv
04:01.0 0401: 1102:0002 (rev 07)
	Subsystem: 1102:8040
	Control: I/O- Mem- BusMaster- SpecCycle- MemWINV- VGASnoop- ParErr- Stepping- SERR- FastB2B- DisINTx-
	Status: Cap+ 66MHz- UDF- FastB2B+ ParErr- DEVSEL=medium >TAbort- <TAbort- <MAbort- >SERR- <PERR- INTx-
	Interrupt: pin A routed to IRQ 255
	Region 0: I/O ports at e000 [disabled] [size=32]
	Capabilities: <access denied>
	Kernel modules: snd_emu10k1



*/






#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/io.h>
#include <unistd.h>
#include <time.h>

int main()
{

    printf("CLOCKS_PER_SECOND: %ld\r\n", CLOCKS_PER_SEC);

    int y = ioperm(0xE000, 32*8, 1);
    printf("%d\r\n", y);


    int i;
    for (i = 0; i < 100; i ++)
    {
        uint32_t x = inl(0xE000 + 4*4);
        clock_t ck = clock();
        printf("%ld :   %d\r\n", (uint64_t) ck, x);
        usleep(100000);
        
        /*
         * RESULT: The 0xE010 register appears to be a simple clock, counting up
         *  at 3,000,000 ticks per second.
         * 
         *  Watch out that the clock() function appears to *NOT* be defined by
         *  CLOCKS_PER_SEC, rather it's 617 ticks per second.
         * 
         */
        
        
    }



/*



    uint32_t  res[32][2];


    int y = ioperm(0xE000, 32*8, 1);
    printf("%d\r\n", y);

    int i;
    for (i = 0; i < 32; i ++)
    {

        uint32_t x = inl(0xE000+i*4);
        res[i][0] = x;
    
    }
    
    
    for (i = 0; i < 32; i ++)
    {

        //outb(0xE000+i, 0x00);
    
    }

    
    for (i = 0; i < 32; i ++)
    {

        uint32_t x = inl(0xE000+i*4);
        res[i][1] = x;
    
    }
  
  
    for (i = 0; i < 32; i ++)
    {

        printf("%03d : %11X\t\t%11X\r\n", i, res[i][0], res[i][1]);

    }
  
  
*/
     /*

    int fd;

    fd = open("/sys/bus/pci/devices/0000:04:01.0/resource0", O_RDWR | O_SYNC);


    void* base_address = (void*)0xe000;
    size_t size = 32;
    void* void_memory = mmap(base_address,
                             size,
                             PROT_READ | PROT_WRITE,
                             MAP_SHARED,
                             fd,
                             0);
    uint16_t* memory = (uint16_t*)void_memory;

    printf("%X\r\n", (uintptr_t)memory);
    * 
    * */

}

