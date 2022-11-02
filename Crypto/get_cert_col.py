#!/usr/bin/env python3
# CMD: ./get_cert_prefix.py cert.cer cer_prefix fastcoll_v1.0.0.5-1_source/fastcoll cert_col1 cert_col2

import sys
import subprocess
import Crypto.Util.number

DEBUG=1

def main():
    if len(sys.argv) != 6:
        print('[USAGE]: ./get_cert_prefix.py <cert.cer_file> <cert_prefix_file> <fastcoll_executable_file> <cert_col1_file> <cert_col2_file>')
        exit(1)

    with open(sys.argv[1], 'rb') as cert_file:
        cert_byte = cert_file.read()
    cert_byte_prefix = cert_byte[:256]

    if DEBUG:
        print('[CERT_BYTE]:        %s'%cert_byte)
        print('[CERT_PREFIX_BYTE]: %s'%cert_byte_prefix)

    with open(sys.argv[2], 'wb') as cert_prefix_file:
        cert_prefix_file.write(cert_byte_prefix)

    CERT_PREFIX_FILE=sys.argv[2]
    FASTCOLL=sys.argv[3]
    CERT_COL1_FILE=sys.argv[4]
    CERT_COL2_FILE=sys.argv[5]
    CERT_COL_CMD='./'+FASTCOLL+' -p '+CERT_PREFIX_FILE+' -o '+CERT_COL1_FILE+' '+CERT_COL2_FILE
    #print(MD5_CMD)
    subprocess.call(CERT_COL_CMD, shell=True)

    with open(CERT_COL1_FILE, 'rb') as cert_col1_file, open(CERT_COL2_FILE, 'rb') as cert_col2_file:
        cert_col1 = cert_col1_file.read()
        cert_col2 = cert_col2_file.read()

    print(Crypto.Util.number.size(int.from_bytes(cert_col1,'little')))

if __name__ == '__main__':
    main()
