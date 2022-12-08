.global _main
.section .text

_main:

push    %ebp
mov     %esp,%ebp

pushl   $0x0068732f # ASCII ' hs/'
pushl   $0x6e69622f # ASCII 'nib/'
movl    %esp,%ebx   # %esp -> %ebx: ptr to start of str '/bin/sh' (const char *filename)
movl    $0x0,%ecx   # ASCII NULL: char *const argv[]
movl    $0x0,%edx   # ASCII NULL: char *const envp[]
movl    $0xb,%eax   # $11 (sys call #) -> %eax

int     $0x80       # invoke system call

leave
ret