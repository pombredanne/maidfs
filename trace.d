#!/usr/sbin/dtrace -s

/*
   Aggregates read(2) and write(2) calls for each unique pathname.
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
    @num["read", path[pid,arg0]] = count();
}

syscall::write*:entry
/path[pid,arg0] != ""/
{
    @num["write", path[pid,arg0]] = count();
}

END
{
    /* print as tab-delimited fields */
    printa("%s\t%s\t%@8u\n", @num);
}
