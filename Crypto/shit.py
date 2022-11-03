from Crypto.Util import number
import math

MODULUS_START_ADDR = 0xC0

with open('cert_col1', 'rb') as cert_col1_file, open('cert_col2', 'rb') as cert_col2_file:
    cert_col1 = cert_col1_file.read()
    cert_col2 = cert_col2_file.read()

# b1 = int.from_bytes(cert_col1[MODULUS_START_ADDR:],'little')
# b2 = int.from_bytes(cert_col2[MODULUS_START_ADDR:],'little')
b1 = int(cert_col1[MODULUS_START_ADDR:].hex(), 16)
b2 = int(cert_col2[MODULUS_START_ADDR:].hex(), 16)
cert_col1_bitsize = b1.bit_length()
cert_col2_bitsize = b2.bit_length()

print('[CERT_COL1_#bit]: %d' % cert_col1_bitsize)
print('[CERT_COL2_#bit]: %d\n' % cert_col2_bitsize)

def getCRT(b1, b2, p1, p2):
    N=p1*p2
    invOne = number.inverse(p2,p1)
    invTwo = number.inverse(p1,p2)
    return -(b1*invOne*p2+b2*invTwo*p1)%N

def Lenstra(b1,b2,e):
    #generate suffix for each certificate
    restart = True
    while(restart):
        flag = False
        while(not flag):
            p1 = number.getPrime(500)
            p2 = number.getPrime(500)
            if(math.gcd(p1-1,e)==1 and math.gcd(p2-1,e)==1):
                flag=True
        b0 = getCRT(b1*(2**1024),b2*(2**1024),p1,p2)
        done = False
        for k in range(b0):
            b = b0+k*p1*p2
            q1 = (b1*2**1024+b)//p1
            q2 = (b2*2**1024+b)//p2
            coprime = (math.gcd(q1-1,e)==1 and math.gcd(q2-1,e)==1)
            if(number.isPrime(q1) and number.isPrime(q2) and coprime):
                done = True
                restart = False
                break
            if(b>=2**1024):
                restart=True
                break
    n1 = b1*2**1024 + b
    n2 = b2*2**1024 + b
    return n1,n2,p1,p2,q1,q2

n1,n2,p1,p2,q1,q2 = Lenstra(b1,b2,e=65537)

print('[p1]:  ',p1)
print('[q1]:  ',q1)
print('[n1]:  ',n1)
print('[p2]:  ',p2)
print('[q2]:  ',q2)
print('[n2]:  ',n2,'\n')