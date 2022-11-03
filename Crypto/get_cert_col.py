#!/usr/bin/env python3
# CMD: ./get_cert_col.py cert.cer cert_DER.cer cer_prefix fastcoll_v1.0.0.5-1_source/fastcoll cert_col1 cert_col2 sol_3.2.5_certA.cer sol_3.2.5_certB.cer sol_3.2.5_factorsA.hex sol_3.2.5_factorsB.hex

'''
RUN ./3.2.5.bash ALSO WORKS
THIS SCRIPT AUTOMATICALLY RUNS EVERYTHING
IT ALSO WRITES RESULTS INTO CORRESPONDING FILES
CHANGE THE FLAGS BELOW TO EXECUTE THE SCRIPT PARTIALLY
GENERATE_CERT_FILE, GENERATE_CERT_COL_FILE, LENSTRAS_ALGORITHM
'''

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
GENERATE_CERT_COL_FILE=0
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
    if len(sys.argv) != 11:
        print('[USAGE]: ./get_cert_prefix.py <cert.cer_file> <cert_DER.cer_file> <cert_prefix_file> <fastcoll_executable_file> <cert_col1_file> <cert_col2_file> <certA.cer_file> <certB.cer_file> <factorsA.hex_file> <factorsB.hex_file>')
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
        cert_file.close()
        cert_DER_file.close()
        print('[INFO]:     try the following command: openssl x509 -in %s -inform der -text -noout'%sys.argv[1])
        print('[INFO]:     Finish generating %s file and %s file (DER encoding) with NetID %s\n'%(sys.argv[1],sys.argv[2],NetID))
    
        print('[INFO]:     Parsing prefix to %s file...'%sys.argv[3])
        with open(sys.argv[3], 'wb') as cert_prefix_file:
            cert_prefix_file.write(cert.tbs_certificate_bytes[:MODULUS_START_ADDR])
        cert_prefix_file.close()

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
            cert_col1_file.close()
            cert_col2_file.close()

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
        cert_col1_file.close()
        cert_col2_file.close()

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

        '''
        p1 = 2649393568965899740506453834030078111529696893210952237224621886962296290010380692683812274435433529077372455755682690394871268428501538630670475968889
        q1 = 4957375429601874496215337211330573955751732296604110179852545273975690784462214493644751909220980279217404162142835874947704640227778719016012929108417788040286345777951316304591845515856518592444090572394997615871741028112399706163343133020973673386185696259857412715806221525623540101983155354787438012183812535869653580218310899456806803322668288898193561765094261283086136625766682209269263217434010858336729120046131905903227875499742295226855615192399787943829
        n1 = 13134038582136770732061675423105679479814702840119061481818103025379166245664336672721025043825404647529509930689207534158767297349477951745001565102117586805261446932861562422073295686900762284035194572123742598609148252137582484713697727592838369632260522988888745658592316889222718575573248930618440705308206377220473244749526820810862354315204836802998993152921094344994768897723309478332493672176012951076973184107870530350393960948506191749283916894184675799707894347832777049413411117758886858081116214801844436785636181691984436073131314237538972929764714023632124653814635581421319837484909584946889883535981
        p2 = 2557033737509999642549168237442256039457845620692893065105010594903428424572992070266124351163383422859925174826312566023304855573762756391582659143527
        q2 = 5136435389752227785843695973846544322234334248569880618014355245613298935012228982391064026688108216997488779410874488119745614153152211753993807887498415263529056255462882937962224255327070062930230327692734830437272168483039500816422664632872563017769178537809345292650467333533025042086696721637534600717084925706992495790169523487843738817400186307093420762802851042491947257926733067093473502722165329052493937456879445821671451162122082271105601407025878581003
        n2 = 13134038582136770732061675423105679479814702837288700795611609009760905632703134707189542626400334935641644966637955337952264643199862604139522775239483401500273141987398939812932801064536393419681469534107926472997557645188917577357112888822528639886426517596214914245600521265388377200413644579684733424021126908576148429106650748520658796915025528535528340191320387513732473973928776761672189555775322205266444029973895588232271249815721954291996576852847430021894082369259820529815914619201997611404320844531371861636791879218211740413078009066647273215106512745480381901294324890712898404958993974504902072617581

        p1_hex = 'cf330f8e90e552adbe99eeab5bbad87eb7551c886f34e224597c088e84df6a0f3854c03fa6f8d7d7b659d06dcd503535357a5c889e5b98e8ba9bce10dc179'
        q1_hex = '808bc51c02d76b9a3882d2cbf3c532b1acb9a2bc7ac5bc732a55e071fbec2a255f4070c983d6f8486547fb6a15e01e17be42bd72781f7d4fecce343dc7ccac03db161d9665e97ed3270b350c5b5d4313c35fdd14ba83cc5cb956a5fcf16e04d3e22fd703c2c3810566084d9b02f57a1e144d3347738dc441baa532b17c4f6e94d5f96ff0e10b85c29dbf29a8154906a65b6a90073fe4fcb7a6c22eab6d3dcef3adde5f1b7700e27d57c0980247e2eac8afd8e398ce266aefb0537b602c2b91d6795'
        n1_hex = '680aa809b1b6800b6d2aaf1a6cf7efe59678ded8da09bd772dca438114028fdc53dcf3d5ced7fac76b2854f9cbd5722c3bcbbc620bce733b3a4c977f3fc45a4805ea4ffed441d2523454cfb31440a9f54f381029429d7a2df68ce1854dcd5ddd8d8ffaf6e39a9f85e25e558aa2aca9bfe0d0e8f98cc6e326bcd768fbbdce0c68006e74e33eccda1990d8e728fea9347d2abc3e8a2db17ddece18affbeacac242ccd3278accdc6557c8829c071a2a88ee30908bfe25c2672f754345d3f27db4fb4acb254e92879d3d4d2958a41136e35d34963aaf76fcb90644fe8ec9e2d1c38513279a6e6f7cac0214f9c209a4a9298ebd66e4e747b8ea701492c88ce18e4a6d'
        p2_hex = 'c7f9f0b0bd11efeb806a6768a7c78f978b6ff3b62639c0b52ed9e5445dfd112ac717e840d332b1e21b330214db01e4b2fffd066a27eeb17b36f668e466767'
        q2_hex = '8530654bb36dbd652d9a845d084bf8b813a08b501c83e6bc3599b83d362d71db8449b29140fe168ac194407d7cc6c629b719c42b6ab611931cf1f86f7bd4f542a4294baf634d2f8b7fd0e2da066e53134c5ce3e82756327a5fea687ddb87dbc9fa5dfbf3630423d4fe5b0458fcba815acbcc910551e8b6d689df9d8923ab441cc604f12a2776b1b8634fab26f1bd0c68de14679075742e47233984fc7ed6f350ef1a5682fbbaa6b6d68b5729b182c565308027f996be8afd218d6483e15e44ebf0b'
        n2_hex = '680aa809b1b6800b6d2aaf1a6cf7efe59678de58da09bd772dca438114028fdc53dcf3d5ced7fac76b2854f9cb55732c3bcbbc620bce733b3a4c97ff3fc45a4805ea4ffed441d2523454cfb31440a9f54f3810a9429d7a2df68ce1854dcd5ddd8d8ffaf6e39a9f85e25e558aa22ca9bfe0d0e8f98cc6e326bcd7687bbdce0c68006e74e33eccda1990d8e728fea9347d2abc3e8a2db17ddece18affbeacac242ccd3278accdc6557c8829c071a2a88ee30908bfe25c2672f754345d3f27db4fb4acb254e92879d3d4d2958a41136e35d34963aaf76fcb90644fe8ec9e2d1c38513279a6e6f7cac0214f9c209a4a9298ebd66e4e747b8ea701492c88ce18e4a6d'
        '''

        print('[INFO]: INT FORMAT of p1,q1,n1 & p2,q2,n2')
        print('[p1]:  ',p1)
        print('[q1]:  ',q1)
        print('[n1]:  ',n1)
        print('[p2]:  ',p2) 
        print('[q2]:  ',q2)
        print('[n2]:  ',n2,'\n')

        print('[INFO]: HEX FORMAT of p1,q1,n1 & p2,q2,n2')
        print('[p1]:  ', hex(p1)[2:])
        print('[q1]:  ', hex(q1)[2:])
        print('[n1]:  ', hex(n1)[2:])
        print('[p2]:  ', hex(p2)[2:])
        print('[q2]:  ', hex(q2)[2:])
        print('[n2]:  ', hex(n2)[2:], '\n')
    
        print('[INFO]: Start generating 2 sets of privkey & pubkey...')
        privkey1 , pubkey1 = mp3_certbuilder.make_privkey(p1,q1)
        privkey2 , pubkey2 = mp3_certbuilder.make_privkey(p2,q2)
        print('[INFO]: Finish generating 2 sets of privkey & pubkey\n')

        print('[INFO]:      Start generating 2 new certificates...')
        certA = mp3_certbuilder.make_cert(NetID, pubkey1)
        print('[MD5_CERTA]:',hashlib.md5(certA.tbs_certificate_bytes).hexdigest())
        certB = mp3_certbuilder.make_cert(NetID, pubkey2)
        print('[MD5_CERTB]:',hashlib.md5(certB.tbs_certificate_bytes).hexdigest(),'\n')

        if hashlib.md5(certA.tbs_certificate_bytes).hexdigest() != hashlib.md5(certB.tbs_certificate_bytes).hexdigest():
            print('[ERROR]: Failed to generate 2 certificates with the SAME MD5 HASH\n')
            exit(1)
        print('[PASS]: SUCCESSFULLY GENERATE 2 CERTIFICATES WITH THE SAME MD5 HASH\n')

        with open(sys.argv[7], 'wb') as certA_file, open(sys.argv[8], 'wb') as certB_file:
            certA_file.write(certA.public_bytes(Encoding.DER))
            certB_file.write(certB.public_bytes(Encoding.DER))
        certA_file.close()
        certB_file.close()
        print('[INFO]:      Finish generating 2 new certificates\n')

        print('[INFO]:      Start writing factors (A&B) into %s file and %s file'%(sys.argv[9],sys.argv[10]))
        with open(sys.argv[9], 'w') as factorsA_file, open(sys.argv[10], 'w') as factorsB_file:
            factorsA_file.write(hex(p1)[2:])
            factorsA_file.write('\n')
            factorsA_file.write(hex(q1)[2:])
            factorsB_file.write(hex(p2)[2:])
            factorsB_file.write('\n')
            factorsB_file.write(hex(q2)[2:])
        factorsA_file.close()
        factorsB_file.close()
        print('[INFO]:      Finish writing factors (A&B) into %s file and %s file\n'%(sys.argv[9],sys.argv[10]))

if __name__ == '__main__':
    main()