.global your_asm_fn
.section .text

your_asm_fn:

push    %ebp
mov     %esp,%ebp

pushl   %eax        # caller save register
pushl   %ecx
pushl   %edx
pushl   %ebx
pushl   %esi
pushl   %edi
pushl   $0xc001f00d # function param mp
pushl   $0xc105ed   # function param sec
pushl   $0xacce55ed # function param app
call    practice
popl    %edi        # restore register
popl    %esi
popl    %ebx
popl    %edx
popl    %ecx
popl    %eax

leave
ret