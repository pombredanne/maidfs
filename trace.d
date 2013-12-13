#!/usr/sbin/dtrace -s

/*
   Dumps read(2) and write(2) calls for each unique pathname with timestamp.
   Field separator can be modified in the 'END' block.
*/

#pragma D option switchrate=10hz
#pragma D option quiet

syscall::open*:entry
{
    self->path = copyinstr(arg0);
}

syscall::open*:return
/self->path != ""/
{
    path[pid,arg0] = self->path;
    self->path = 0;
}

syscall::read*:entry
/path[pid,arg0] != ""/
{
    printf("read\t%s\t%u\t%u\n", path[pid,arg0], timestamp, arg2);
}

syscall::write*:entry
/path[pid,arg0] != ""/
{
    printf("write\t%s\t%u\t%u\n", path[pid,arg0], timestamp, arg2);
}
