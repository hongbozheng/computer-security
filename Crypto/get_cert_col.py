#!/usr/bin/env python3
# CMD: ./get_cert_col.py cert.cer cer_prefix fastcoll_v1.0.0.5-1_source/fastcoll cert_col1 cert_col2 sol_3.2.5_certA.cer sol_3.2.5_certB.cer

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
    if len(sys.argv) != 8:
        print('[USAGE]: ./get_cert_prefix.py <cert.cer_file> <cert_prefix_file> <fastcoll_executable_file> <cert_col1_file> <cert_col2_file> <certA.cer_file> <certB.cer_file>')
        exit(1)
    '''
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

    with open(sys.argv[1], 'wb') as cert_file:
        cert_file.write(cert.public_bytes(Encoding.DER))
    print('[INFO]:     try the following command: openssl x509 -in %s -inform der -text -noout'%sys.argv[1])
    print('[INFO]:     Finish generating %s file with NetID %s\n'%(sys.argv[1],NetID))

    print('[INFO]:     Parsing prefix to %s file...'%sys.argv[2])
    with open(sys.argv[2], 'wb') as cert_prefix_file:
        cert_prefix_file.write(cert.tbs_certificate_bytes[:MODULUS_START_ADDR])

    if DEBUG:
        print('[CERT_BYTE]:        %s'%cert.tbs_certificate_bytes)
        print('[CERT_PREFIX_BYTE]: %s'%cert.tbs_certificate_bytes[:MODULUS_START_ADDR])
    
    print('[INFO]: Finish writing into %s file and %s file\n'%(sys.argv[1],sys.argv[2]))

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

        #b1 = int.from_bytes(cert_col1[MODULUS_START_ADDR:],'little')
        #b2 = int.from_bytes(cert_col2[MODULUS_START_ADDR:],'little')
        b1 = int(cert_col1[MODULUS_START_ADDR:].hex(),16)
        b2 = int(cert_col2[MODULUS_START_ADDR:].hex(),16)
        cert_col1_bitsize = Crypto.Util.number.size(b1)
        cert_col2_bitsize = Crypto.Util.number.size(b2)
        print('[CERT_COL1_#bit]: %d'%cert_col1_bitsize)
        print('[CERT_COL2_#bit]: %d\n'%cert_col2_bitsize)

        if cert_col1_bitsize == 1023 and cert_col2_bitsize == 1023:
            break

    print('[INFO]: Found 2 cert_col str both with length 1023 bit')
    print('---------------------------------------------------------------------------\n')

    '''
    with open(sys.argv[4], 'rb') as cert_col1_file, open(sys.argv[5], 'rb') as cert_col2_file:
        cert_col1 = cert_col1_file.read()
        cert_col2 = cert_col2_file.read()
    
    # b1 = int.from_bytes(cert_col1[MODULUS_START_ADDR:],'little')
    # b2 = int.from_bytes(cert_col2[MODULUS_START_ADDR:],'little')
    b1 = int(cert_col1[MODULUS_START_ADDR:].hex(),16)
    b2 = int(cert_col2[MODULUS_START_ADDR:].hex(),16)
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
    
    print('[INFO]: Start running Lenstra Algorithm...')
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
    '''
    p1 = 2410836382960508330241485431149720581862579210353992702695999302778740226565869145747463351696244659173480645034530663095414455703939063586508907851377
    q1 = 5573183460591385119759401936054274808036180644480349619887489881375472293061134042652194555128560041259076123569685154816563552620773528449323130493763196994027709689664610984530866736343642151765877292211695946830870707740032048323747012304961989224402727774619304876784133323717344172002092682485471005783550739666637795694157346326732563214297783089302846309708056452358447992562694478535180958064711622177472110269613446263959240897518495017706667207150929215251
    n1 = 13436033455707463622351488018625238810316679320415619412845612953580157798144824519923695838768677104058514668799304601008227201812339461283714798659515385778356953094285889971347710552356130272269615247377179769213286508976159411296297589141421873816156034428738757507602445998285514546012281039275853100267049562056612699793989714318251875783470921802439669081206096070159006821108576196654665817009569964418837613006784213338887252136654397434952448888477072304758281401746545261794158389635728488058159098360528711165521012871288494520513899866599594233957133119167564359062640611090627536997534706768403149750627

    p2 = 2872884571299948711848945936719067197472535530629693735202579393459758892215555672543878922091319966020258202359955867367007540665050934332771378739301
    q2 = 4676844169074222870445921912156226662287112620300020110192137762231199235457077944589150537678167268334779178084672019622158930904751686385268971562971230864050311194810901098697111129801667987977436573850769976998121779192768979635903555124568053874596309477974296828856928621476950773396036510298720427940686248749966112323783139379042732458091733149107528574142003812312944338314462748107873082799706623135611618549928844530243153186844141370018836030414460363303
    n2 = 13436033455707463622351488018625238810316679317585258726639118937961897185183622554392213421343607392170649718508293837070590937818921039468027785692475993591843353737912134738057147516878213000899052444899764125862375649991542774654450045669339013299918201190300476820033975024744484089606344876593332291656080707245826183972084763152518108643590777922229237353321613652015197918630826651994988710273761834885704360041777853464020882379484134150792739220946925779301451103357485299592793889786119688865481302429965059749809151169507120116362977891646020252707382613797957465218915799366087134004857346160902584271203
    '''

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

    with open(sys.argv[6], 'wb') as certA_file, open(sys.argv[7], 'wb') as certB_file:
        certA_file.write(certA.public_bytes(Encoding.DER))
        certB_file.write(certB.public_bytes(Encoding.DER))

    print('[INFO]:      Finish generating 2 new certificates\n')
    
if __name__ == '__main__':
    main()
