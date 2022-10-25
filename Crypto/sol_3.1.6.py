#!/usr/bin/env python3
# CMD: python3 sol_3.1.6.py 3.1.6_input_string.txt sol_3.1.6.hex
# TEST_CMD: python3 sol_3.1.6.py sol_3.1.6.txt sol_3.1.6.hex

import sys

DEBUG=False

def WHA(byte_str):
    mask = 0x3FFFFFFF
    wha_hash = 0
    for byte in byte_str:
        inter_val = ((byte ^ 0xCC) << 24) | ((byte ^ 0x33) << 16) | ((byte ^ 0xAA) << 8) | (byte ^ 0x55)
        wha_hash = (wha_hash & mask) + (inter_val & mask)
    return wha_hash

def main():
    if len(sys.argv) != 3:
        print('[USAGE]: python3 <your_script.py> <file.txt> <output_file>')
        exit()

    with open(sys.argv[1], 'r') as f:
        input_str = f.read().strip()

    byte_str = bytes(input_str, 'UTF-8')
    wha_hash = WHA(byte_str=byte_str)

    if DEBUG:
        print('[INPUT_BYTE]:   %s'%byte_str)
        print('[WHA_HAS]:      %d'%wha_hash)
        print('[WHA_HASH_HEX]: %s'%hex(wha_hash))

    with open(sys.argv[2], 'w') as out:
        out.write(hex(wha_hash)[2:])

if __name__ == '__main__':
    main()
