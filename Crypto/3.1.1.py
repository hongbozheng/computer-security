#!/usr/bin/env python3

FILE_HEX_STR = '3.1.1_value.hex'

def main():
    with open(FILE_HEX_STR, 'r') as f:
        hex_str = f.read().strip()
        int_ = int(hex_str,16)
        bin_ = bin(int_)[2:]
        print('[HEX_STR]: %s'%hex_str)
        print('[INT]:     %d'%int_)
        print('[BIN]:     %s'%bin_)

if __name__ == '__main__':
    main()