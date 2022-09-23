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
pushl   $0          # ASCII NULL (EOS)
pushl   $0x646f6f66 # ASCII 'doof'
pushl   $0x6c6f6f63 # ASCII 'looc'
movl    %esp,%ebx   # %esp -> %ebx: ptr to start of str 'coolfood'
pushl   $0xc105ed
movl    %esp,%esi   # %esp -> %esi: ptr to $0xc105ed
pushl   %ebx        # function param *mp
pushl   %esi        # function param *sec
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
