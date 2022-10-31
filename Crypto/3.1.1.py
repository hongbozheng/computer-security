#!/usr/bin/env python3

HEX_STR_FILE = '3.1.1_value.hex'

def main():
    with open(HEX_STR_FILE, 'r') as f:
        hex_str = f.read().strip()

    int_ = int(hex_str,16)
    bin_ = bin(int_)[2:]

    print('[HEX_STR]: %s'%hex_str)
    print('[INT]:     %d'%int_)
    print('[BIN]:     %s'%bin_)

if __name__ == '__main__':
    main()