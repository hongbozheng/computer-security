#!/usr/bin/env python3
# CMD: ./sol_3.2.4.py 3.2.4_ciphertext.enc.asc moduli.hex sol_3.2.4.txt
'''
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
REMEMBER TO EITHER 'ADD A NEW LINE IN FILE <3.2.4_ciphertext.enc.asc>'
OR REMOVE THE '\n' CHARACTER FROM THE VARIABLE 'encrypt_footer' IN FILE <pbp.py>
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

Reference:
get_product_tree(int_list): https://facthacks.cr.yp.to/product.html
get_rem_tree(int,int_list): https://facthacks.cr.yp.to/remainder.html
get_gcd():                  https://facthacks.cr.yp.to/batchgcd.html
egcd() & modinv():          https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
'''

import sys
import pbp
from math import gcd
from Crypto.PublicKey import RSA
from Crypto.Util import number

e = int(65537)
DEBUG=1

def get_prod_tree(int_list):
    prod_tree = [int_list]
    while len(prod_tree[-1]) > 1:
        int_list = prod_tree[-1]
        int_list_len = len(int_list)
        prod_tmp = [int_list[i*2]*int_list[i*2+1] for i in range(int_list_len//2)]
        if int_list_len%2 == 1:
            prod_tmp.append(int_list[int_list_len-1])
        prod_tree.append(prod_tmp)
    return prod_tree

def get_gcd(int_list):
    prod_tree = get_prod_tree(int_list=int_list)
    rem_tree = prod_tree.pop()
    while prod_tree:
        int_list = prod_tree.pop()
        rem_tree = [rem_tree[i//2]%int_list[i]**2 for i in range(len(int_list))]
    return [gcd(rem//n,n) for rem,n in zip(rem_tree,int_list)]

def get_d(p, q, e):
    return number.inverse(u=e, v=(p-1)*(q-1))

def find_pvt_key(gcd_list, moduli):
    pvt_key = []
    for i in range(len(gcd_list)):
        if gcd_list[i] != 1:
            p = gcd_list[i]
            N = moduli[i]
            d = get_d(p=p, q=N//p, e=e)
            pvt_key.append(RSA.construct((int(N), int(e), int(d))))
    return pvt_key

def get_result(pvt_key, cipher):
    plaintext = ''
    for key in pvt_key:
        try:
            plaintext = pbp.decrypt(rsakey=key, c=cipher)
        except ValueError:
            pass
    return plaintext

def main():
    if len(sys.argv) != 4:
        print('[USAGE]: ./sol_3.2.4.py <ciphertext.enc.asc_file> <moduli.hex_file> <decrypted_msg_file>')
        exit(1)

    with open(sys.argv[1], 'r') as ciphertxt_enc_asc_file, open(sys.argv[2], 'r') as moduli_hex_file:
        ciphertxt_enc_asc = ciphertxt_enc_asc_file.read()
        if DEBUG: print('[CIPHER]: %s'%ciphertxt_enc_asc)
        if DEBUG: print('[INFO]: Read & Convert MODULI from HEX to INT')
        moduli = [int(i.strip(),16) for i in moduli_hex_file.readlines()]

    if DEBUG: print('[INFO]: Performing FAST BATCH GCD...')
    gcd_list = get_gcd(int_list=moduli)
    if DEBUG: print('[INFO]: Finish Calculating GCD')

    if DEBUG: print('[INFO]: Calculating PRIVATE KEY...')
    pvt_key = find_pvt_key(gcd_list=gcd_list, moduli=moduli)
    if DEBUG: print('[INFO]: Finish Calculating PRIVATE KEY')

    if DEBUG: print('[INFO]: Decrypting Final Result...')
    decrypted_byte = get_result(pvt_key=pvt_key, cipher=ciphertxt_enc_asc)
    decrypted_msg = decrypted_byte.decode(encoding='UTF-8',errors='strict')
    if DEBUG:
        print('[PLAINBYTE]: %s'%decrypted_byte)
        print('[PLAINTEXT]: %s'%decrypted_msg)

    with open(sys.argv[3], 'w') as decrypted_msg_file:
        decrypted_msg_file.write(decrypted_msg)

if __name__ == '__main__':
    main()