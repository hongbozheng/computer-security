#!/usr/bin/env python3
# CMD: ./get_cert_col.py cert.cer cert_DER.cer cer_prefix fastcoll_v1.0.0.5-1_source/fastcoll cert_col1 cert_col2 sol_3.2.5_certA.cer sol_3.2.5_certB.cer

import sys
import subprocess
import Crypto.Util.number
import math
import mp3_certbuilder
import hashlib
from cryptography.hazmat.primitives.serialization import Encoding

e=65537
MODULUS_START_ADDR=0xC0
NetID='hongboz2'
GENERATE_CERT_FILE=0
GENERATE_CERT_COL_FILE=1
LENSTRAS_ALGORITHM=0
DEBUG=1

def getCoprimes():
    bitsize = 500
    p1, p2 = -1, -1
    
    while (p1 == p2) or (math.gcd(e, p1-1)!=1) or (math.gcd(e, p2-1)!=1):
        p1 = Crypto.Util.number.getPrime(bitsize)
        p2 = Crypto.Util.number.getPrime(bitsize)
    
    return p1, p2

def getCRT(b1, b2, p1, p2):
    N=p1*p2
    invOne = Crypto.Util.number.inverse(p2,p1)
    invTwo = Crypto.Util.number.inverse(p1,p2)
    return -(b1*invOne*p2+b2*invTwo*p1)%N

def main():
    if len(sys.argv) != 9:
        print('[USAGE]: ./get_cert_prefix.py <cert.cer_file> <cert_DER.cer_file> <cert_prefix_file> <fastcoll_executable_file> <cert_col1_file> <cert_col2_file> <certA.cer_file> <certB.cer_file>')
        exit(1)
    
    if GENERATE_CERT_FILE:
        print('[INFO]:     Generating %s file with NetID %s...'%(sys.argv[1],NetID))
        while 1:
            p = Crypto.Util.number.getPrime(1024)
            q = Crypto.Util.number.getPrime(1024)
            if (p*q).bit_length() == 2047:
                break
        assert ((p*q).bit_length() == 2047)
        privkey, pubkey = mp3_certbuilder.make_privkey(p, q)
        cert = mp3_certbuilder.make_cert(NetID, pubkey)
        print('[MD5_CERT]:', hashlib.md5(cert.tbs_certificate_bytes).hexdigest())

        with open(sys.argv[1], 'wb') as cert_file, open('cert_DER.cer', 'wb') as cert_DER_file:
            cert_file.write(cert.tbs_certificate_bytes)
            cert_DER_file.write(cert.public_bytes(Encoding.DER))
        print('[INFO]:     try the following command: openssl x509 -in %s -inform der -text -noout'%sys.argv[1])
        print('[INFO]:     Finish generating %s file and %s file (DER encoding) with NetID %s\n'%(sys.argv[1],sys.argv[2],NetID))
    
        print('[INFO]:     Parsing prefix to %s file...'%sys.argv[3])
        with open(sys.argv[3], 'wb') as cert_prefix_file:
            cert_prefix_file.write(cert.tbs_certificate_bytes[:MODULUS_START_ADDR])

        if DEBUG:
            print('[CERT_BYTE]:        %s'%cert.tbs_certificate_bytes)
            print('[CERT_PREFIX_BYTE]: %s'%cert.tbs_certificate_bytes[:MODULUS_START_ADDR])
    
        print('[INFO]: Finish generating prefix to %s file\n'%sys.argv[3])
    
    if GENERATE_CERT_FILE:
        exit(0)

    if GENERATE_CERT_COL_FILE:
        CERT_PREFIX_FILE=sys.argv[3]
        FASTCOLL=sys.argv[4]
        CERT_COL1_FILE=sys.argv[5]
        CERT_COL2_FILE=sys.argv[6]
        CERT_COL_CMD='./'+FASTCOLL+' -p '+CERT_PREFIX_FILE+' -o '+CERT_COL1_FILE+' '+CERT_COL2_FILE
    
        print('[INFO]: Executing fastcoll until both 2 cert_col str length are 1023 in bit...')
        while 1:
            print('[INFO]: Executing fastcoll...')
            subprocess.call(CERT_COL_CMD, shell=True)
            print('[INFO]: Finish executing fastcoll\n')
            with open(CERT_COL1_FILE, 'rb') as cert_col1_file, open(CERT_COL2_FILE, 'rb') as cert_col2_file:
                cert_col1 = cert_col1_file.read()
                cert_col2 = cert_col2_file.read()

            b1 = int(cert_col1[MODULUS_START_ADDR:].hex(),16)
            b2 = int(cert_col2[MODULUS_START_ADDR:].hex(),16)
            cert_col1_bitsize = b1.bit_length()
            cert_col2_bitsize = b2.bit_length()
            print('[CERT_COL1_#bit]: %d'%cert_col1_bitsize)
            print('[CERT_COL2_#bit]: %d\n'%cert_col2_bitsize)

            if cert_col1_bitsize == 1023 and cert_col2_bitsize == 1023:
                break
        
        assert cert_col1_bitsize == 1023
        assert cert_col2_bitsize == 1023
        print('[INFO]: Found 2 cert_col byte-files both with bit length 1023 bit')
        print('---------------------------------------------------------------------------\n')
    
    if GENERATE_CERT_COL_FILE:
        exit(0)
    
    if LENSTRAS_ALGORITHM:
        print('[INFO]: Start Lenstra Algorithm...')
        print('[INFO]: Read from %s file and %s file to get b1 & b2'%(sys.argv[5],sys.argv[6]))
        with open(sys.argv[5], 'rb') as cert_col1_file, open(sys.argv[6], 'rb') as cert_col2_file:
            cert_col1 = cert_col1_file.read()
            cert_col2 = cert_col2_file.read()
    
        b1 = int(cert_col1[MODULUS_START_ADDR:].hex(),16)
        b2 = int(cert_col2[MODULUS_START_ADDR:].hex(),16)
        cert_col1_bitsize = b1.bit_length()
        cert_col2_bitsize = b2.bit_length()
        
        assert cert_col1_bitsize == 1023
        assert cert_col2_bitsize == 1023
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
        print('[INFO]: Finish Iteration\n')

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
        certA = mp3_certbuilder.make_cert(NetID, pubkey1)
        print('[MD5_CERTA]:',hashlib.md5(certA.tbs_certificate_bytes).hexdigest())
        certB = mp3_certbuilder.make_cert(NetID, pubkey2)
        print('[MD5_CERTB]:',hashlib.md5(certB.tbs_certificate_bytes).hexdigest())

        with open(sys.argv[7], 'wb') as certA_file, open(sys.argv[8], 'wb') as certB_file:
            certA_file.write(certA.public_bytes(Encoding.DER))
            certB_file.write(certB.public_bytes(Encoding.DER))

        print('[INFO]:      Finish generating 2 new certificates\n')
    
if __name__ == '__main__':
    main()
