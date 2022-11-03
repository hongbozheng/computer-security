#!/usr/bin/env python3
# CMD: ./get_cert_prefix.py cert.cer cer_prefix fastcoll_v1.0.0.5-1_source/fastcoll cert_col1 cert_col2

import sys
import subprocess
import Crypto.Util.number
from math import gcd
import mp3_certbuilder
import hashlib

DEBUG=1


def getCoprimes(e=65537):
    bitsize = 500
    p1, p2 = -1, -1
    
    while (p1 == p2) or not (gcd(e, p1-1)==1) or not (gcd(e, p2-1)==1):
        p1 = Crypto.Util.number.getPrime(bitsize)
        p2 = Crypto.Util.number.getPrime(bitsize)
    
    assert (gcd(e,p1-1) == 1)
    assert (gcd(e,p2-1) == 1)
    return p1, p2

def getCRT(b1, b2, p1, p2):
    N=p1*p2
    invone = Crypto.Util.number.inverse(p2,p1)
    invtwo = Crypto.Util.number.inverse(p1,p2)
    return -(b1*invone*p2*invtwo*p1)%N


def main():
    if len(sys.argv) != 6:
        print('[USAGE]: ./get_cert_prefix.py <cert.cer_file> <cert_prefix_file> <fastcoll_executable_file> <cert_col1_file> <cert_col2_file>')
        exit(1)

    with open(sys.argv[1], 'rb') as cert_file:
        cert_byte = cert_file.read()
    cert_byte_prefix = cert_byte[:256]

    if DEBUG:
        print('[CERT_BYTE]:        %s'%cert_byte)
        print('[CERT_PREFIX_BYTE]: %s\n'%cert_byte_prefix)

    with open(sys.argv[2], 'wb') as cert_prefix_file:
        cert_prefix_file.write(cert_byte_prefix)

    CERT_PREFIX_FILE=sys.argv[2]
    FASTCOLL=sys.argv[3]
    CERT_COL1_FILE=sys.argv[4]
    CERT_COL2_FILE=sys.argv[5]
    CERT_COL_CMD='./'+FASTCOLL+' -p '+CERT_PREFIX_FILE+' -o '+CERT_COL1_FILE+' '+CERT_COL2_FILE
    
    print('[INFO]: Executing fastcoll until both 2 cert_col str length are 1023 in bit...')
    while 1:
        print('[INFO]: Executing fastcoll...')
        subprocess.call(CERT_COL_CMD, shell=True)
        print('[INFO]: Finish executing fastcoll\n')
        with open(CERT_COL1_FILE, 'rb') as cert_col1_file, open(CERT_COL2_FILE, 'rb') as cert_col2_file:
            cert_col1 = cert_col1_file.read()
            cert_col2 = cert_col2_file.read()

        b1 = int.from_bytes(cert_col1[256:],'little')
        b2 = int.from_bytes(cert_col2[256:],'little')
        cert_col1_bitsize = Crypto.Util.number.size(b1)
        cert_col2_bitsize = Crypto.Util.number.size(b2)
        print('[CERT_COL1_#bit]: %d'%cert_col1_bitsize)
        print('[CERT_COL2_#bit]: %d\n'%cert_col2_bitsize)

        if cert_col1_bitsize == 1023 and cert_col2_bitsize == 1023:
            break

    print('[INFO]: Found 2 cert_col str both with length 1023 bit')
    print('----------------------------------------------------------------------')
    
    b1 *= 2**1024
    b2 *= 2**1024
    assert Crypto.Util.number.size(b1) == 2047
    assert Crypto.Util.number.size(b2) == 2047
    p1, p2 = getCoprimes()
    b0 = getCRT(b1,b2,p1,p2)

    k,b = 0,0

    while(Crypto.Util.number.size(b) <= 1024):
        b = b0+k*p1*p2
        q1 = (b1+b)//p1
        q2 = (b2+b)//p2
        if (Crypto.Util.number.isPrime(q1) and Crypto.Util.number.isPrime(q2)):
            break
        else:
            k += 1
            print('[INFO]: Iteration %d'%k)

    print('q1',q1)
    print('q2',q2)
    print('p1',p1)
    print('p2',p2)

    assert (p1*q2).bit_length()
    assert (Crypto.Util.number.isPrime(q1) == 1)
    assert (Crypto.Util.number.isPrime(q2) == 1)
    
    print('b',b)
    n1 = b1+b
    n2 = b2+b
    print('n1',n1)

    privkey1 , pubkey1 = mp3-certbuilder.make_privkey(p1,q1)
    privkey2 , pubkey2 = mp3-certbuilder.make_privkey(p2,q2)

    cert1 = mp3-certbuilder.make_cert('hongboz2', pubkey1)
    print('md5 of cert1',hashlib.md5(cert1.tbs_certificate_bytes).hexdigest())
    cert2 = mp3-certbuilder.make_cert('hongboz2', pubkey2)
    print('md5 of cert2',hashlib.md5(cert2.tbs_certificate_bytes).hexdigest())
    

if __name__ == '__main__':
    main()
