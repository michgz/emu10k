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

int main()
{


    int y = ioperm(0xE000, 32*8, 1);
    printf("%d\r\n", y);

    int i;
    for (i = 0; i < 32; i ++)
    {

        uint16_t x = inb(0xE000+i);
        printf("%03d : %X\r\n", i, x);
    
    }
    
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
