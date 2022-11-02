#!/usr/bin/env python3
# CMD: ./get_cert_prefix.py cert.cer cer_prefix fastcoll_v1.0.0.5-1_source/fastcoll md5_1 md5_2

import sys
import subprocess
import Crypto.Util.number

DEBUG=1

def main():
    if len(sys.argv) != 6:
        print('[USAGE]: ./get_cert_prefix.py <cert.cer_file> <cert_prefix_file> <fastcoll_executable_file> <md5_hash_1_file> <md5_hash_2_file>')
        exit(1)

    with open(sys.argv[1], 'rb') as cert_file:
        cert_byte = cert_file.read()
    cert_byte_prefix = cert_byte[:256]

    if DEBUG:
        print('[CERT_BYTE]:        %s'%cert_byte)
        print('[CERT_PREFIX_BYTE]: %s'%cert_byte_prefix)

    with open(sys.argv[2], 'wb') as cert_byte_prefix_file:
        cert_byte_prefix_file.write(cert_byte_prefix)

    CERT_PREFIX_FILE=sys.argv[2]
    FASTCOLL=sys.argv[3]
    MD5_1_FILE=sys.argv[4]
    MD5_2_FILE=sys.argv[5]
    MD5_CMD='./'+FASTCOLL+' -p '+CERT_PREFIX_FILE+' -o '+MD5_1_FILE+' '+MD5_2_FILE
    print(MD5_CMD)
    subprocess.call(MD5_CMD, shell=True)

if __name__ == '__main__':
    main()