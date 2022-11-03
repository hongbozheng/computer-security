#!/usr/bin/env python3
# CMD: ./get_cert_col.py cert.cer cer_prefix fastcoll_v1.0.0.5-1_source/fastcoll cert_col1 cert_col2 sol_3.2.5_certA.cer sol_3.2.5_certB.cer

import sys
import subprocess
import Crypto.Util.number
import math
import mp3_certbuilder
import hashlib

e=65537
MODULUS_START_ADDR=0xC0
NetID = 'hongboz2'
DEBUG=1

def getCoprimes():
    bitsize = 500
    p1, p2 = -1, -1
    
    while (p1 == p2) or not (math.gcd(e, p1-1)==1) or not (math.gcd(e, p2-1)==1):
        p1 = Crypto.Util.number.getPrime(bitsize)
        p2 = Crypto.Util.number.getPrime(bitsize)
    
    return p1, p2

def getCRT(b1, b2, p1, p2):
    N=p1*p2
    invOne = Crypto.Util.number.inverse(p2,p1)
    invTwo = Crypto.Util.number.inverse(p1,p2)
    return -(b1*invOne*p2+b2*invTwo*p1)%N

def main():
    if len(sys.argv) != 8:
        print('[USAGE]: ./get_cert_prefix.py <cert.cer_file> <cert_prefix_file> <fastcoll_executable_file> <cert_col1_file> <cert_col2_file> <certA.cer_file> <certB.cer_file>')
        exit(1)

    with open(sys.argv[1], 'rb') as cert_file:
        cert_byte = cert_file.read()
    cert_byte_prefix = cert_byte[:MODULUS_START_ADDR]

    if DEBUG:
        print('[CERT_BYTE]:        %s'%cert_byte)
        print('[CERT_PREFIX_BYTE]: %s'%cert_byte_prefix)

    with open(sys.argv[2], 'wb') as cert_prefix_file:
        cert_prefix_file.write(cert_byte_prefix)
    
    print('[INFO]: Finish writing into %s file\n'%sys.argv[2])

    CERT_PREFIX_FILE=sys.argv[2]
    FASTCOLL=sys.argv[3]
    CERT_COL1_FILE=sys.argv[4]
    CERT_COL2_FILE=sys.argv[5]
    CERT_COL_CMD='./'+FASTCOLL+' -p '+CERT_PREFIX_FILE+' -o '+CERT_COL1_FILE+' '+CERT_COL2_FILE
    '''
    print('[INFO]: Executing fastcoll until both 2 cert_col str length are 1023 in bit...')
    while 1:
        print('[INFO]: Executing fastcoll...')
        subprocess.call(CERT_COL_CMD, shell=True)
        print('[INFO]: Finish executing fastcoll\n')
        with open(CERT_COL1_FILE, 'rb') as cert_col1_file, open(CERT_COL2_FILE, 'rb') as cert_col2_file:
            cert_col1 = cert_col1_file.read()
            cert_col2 = cert_col2_file.read()

        b1 = int.from_bytes(cert_col1[MODULUS_START_ADDR:],'little')
        b2 = int.from_bytes(cert_col2[MODULUS_START_ADDR:],'little')
        cert_col1_bitsize = Crypto.Util.number.size(b1)
        cert_col2_bitsize = Crypto.Util.number.size(b2)
        print('[CERT_COL1_#bit]: %d'%cert_col1_bitsize)
        print('[CERT_COL2_#bit]: %d\n'%cert_col2_bitsize)

        if cert_col1_bitsize == 1023 and cert_col2_bitsize == 1023:
            break

    print('[INFO]: Found 2 cert_col str both with length 1023 bit')
    print('---------------------------------------------------------------------------\n')
    '''
    with open(CERT_COL1_FILE, 'rb') as cert_col1_file, open(CERT_COL2_FILE, 'rb') as cert_col2_file:
        cert_col1 = cert_col1_file.read()
        cert_col2 = cert_col2_file.read()

    b1 = int.from_bytes(cert_col1[MODULUS_START_ADDR:],'little')
    b2 = int.from_bytes(cert_col2[MODULUS_START_ADDR:],'little')
    cert_col1_bitsize = b1.bit_length()
    cert_col2_bitsize = b2.bit_length()

    print('[CERT_COL1_#bit]: %d'%cert_col1_bitsize)
    print('[CERT_COL2_#bit]: %d\n'%cert_col2_bitsize)

    b1 *= 2**1024
    b2 *= 2**1024
    assert Crypto.Util.number.size(b1) == 2047
    assert Crypto.Util.number.size(b2) == 2047

    p1, p2 = getCoprimes()
    assert (math.gcd(e,p1-1) == 1)
    assert (math.gcd(e,p2-1) == 1)

    b0 = getCRT(b1,b2,p1,p2)
    k,b = 0,0
    while(Crypto.Util.number.size(b) <= 1024):
        b = b0+k*p1*p2
        q1 = (b1+b)//p1
        q2 = (b2+b)//p2
        if Crypto.Util.number.isPrime(q1) and Crypto.Util.number.isPrime(q2) and (math.gcd(e,q1-1)==1) and (math.gcd(e,q2-1)==1):
            break
        else:
            k += 1
            print('[INFO]: Iteration %d'%k)
    
    assert Crypto.Util.number.isPrime(q1)
    assert Crypto.Util.number.isPrime(q2)
    assert (math.gcd(e,q1-1)==1)
    assert (math.gcd(e,q2-1)==1)

    n1 = b1+b
    n2 = b2+b

    print('[p1]:  ',p1)
    print('[q1]:  ',q1)
    print('[n1]:  ',n1)
    print('[p2]:  ',p2) 
    print('[q2]:  ',q2)
    print('[n2]:  ',n2,'\n')
    
    print('[INFO]: Start generating 2 sets of privkey & pubkey...')
    privkey1 , pubkey1 = mp3_certbuilder.make_privkey(p1,q1)
    privkey2 , pubkey2 = mp3_certbuilder.make_privkey(p2,q2)
    print('[INFO]: Finish generating 2 sets of privkey & pubkey\n')

    print('[INFO]:      Start generating 2 new certificates...')
    cert1 = mp3_certbuilder.make_cert(NetID, pubkey1)
    print('[MD5_CERT1]:',hashlib.md5(cert1.tbs_certificate_bytes).hexdigest())
    cert2 = mp3_certbuilder.make_cert(NetID, pubkey2)
    print('[MD5_CERT2]:',hashlib.md5(cert2.tbs_certificate_bytes).hexdigest())

    with open(sys.argv[6], 'wb') as certA_file, open(sys.argv[7], 'wb') as certB_file:
        certA_file.write(cert.public_bytes(Encoding.DER))
        certB_file.write(cert.public_bytes(Encoding.DER))

    print('[INFO]:      Finish generating 2 new certificates\n')
    
if __name__ == '__main__':
    main()
