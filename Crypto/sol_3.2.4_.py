#!/usr/bin/env python3
# CMD: ./sol_3.2.4.py 3.2.4_ciphertext.enc.asc moduli.hex
import fractions
import sys

import pbp
from math import floor, gcd
# from fractions import gcd
from Crypto.PublicKey import RSA

DEBUG=1

# Sources:
# product_tree(): https://facthacks.cr.yp.to/product.html
# remainder_tree(0): https://facthacks.cr.yp.to/remainder.html
# find_gcds(): https://facthacks.cr.yp.to/batchgcd.html
# egcd() and modinv(): https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python

def calc_prod_tree(int_list):
    prod_tree = [int_list]
    # print(int_list)
    while len(prod_tree[-1]) > 1:
        int_list = prod_tree[-1]
        int_list_len = len(int_list)
        prod_tmp = [int_list[i*2]*int_list[i*2+1] for i in range(int_list_len//2)]
        if int_list_len % 2 == 1:
            prod_tmp.append(int_list[int_list_len-1])
        prod_tree.append(prod_tmp)
    return prod_tree[-1][0], prod_tree
    # print(prod_tree, prod_tree[-1][0])

def sq_prod_tree(prod_tree):
    prod_tree_sq = []
    for i in range(len(prod_tree)):
        prod_tree_sq.append([prod_tree[i][j]**2 for j in range(len(prod_tree[i]))])
    return prod_tree_sq

def calc_rem_tree(prod, prod_tree):
    rem = [prod]
    for node in reversed(prod_tree):
        rem = [rem[i//2] % node[i] for i in range(len(node))]
    return rem

def cal_gcd(rem_tree, moduli_list):
    V = [gcd(rem//n,n) for rem,n in zip(rem_tree,moduli_list)]
    result = []
    for i in range(len(V)):
        if V[i] != 1:
            result.append((V[i],moduli_list[i]))
    return result

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b%a, a)
        return (g, x-(b//a)*y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse DNE')
    else:
        return x % m

def find_pvt_key(moduli):
    e = int(65537)
    pvt_key = []
    for i in range(len(moduli)):
        p = moduli[i][0]
        N = moduli[i][1]
        q = N//p

        try:
            d = modinv(e, (p-1)*(q-1))
            pvt_key.append(RSA.construct((int(N), int(e), int(d))))
        except:
            pass
    return pvt_key

def get_result(pvt_key, cipher):
    # print(pvt_key)
    for key in pvt_key:
        try:
            plaintext = pbp.decrypt(key, cipher)
            print(plaintext)
        except ValueError:
            pass

calc_prod_tree([1,2,3,4,5,6,7])

def main():
    if len(sys.argv) != 3:
        print('[USAGE]: ./sol_3.2.4.py <ciphertext.enc.asc_file> <moduli.hex_file>')
        exit(1)

    with open(sys.argv[1], 'r') as cipher_file, open(sys.argv[2], 'r') as moduli_hex_file:
        cipher = cipher_file.read().replace('\r\n', '\n')
        moduli_list = [i.strip() for i in moduli_hex_file.readlines()]
    if DEBUG: print('[CIPHER]: %s'%cipher)

    if DEBUG: print('[INFO]: Convert moduli_list from HEX to INT')
    moduli_list = [int(i,16) for i in moduli_list]

    if DEBUG: print('[INFO]: Calculating Product Tree...')
    prod, prod_tree = calc_prod_tree(int_list=moduli_list)
    if DEBUG: print('[INFO]: Finish Calculating Product Tree')

    if DEBUG: print('[INFO]: Calculating Squares...')
    prod_tree = sq_prod_tree(prod_tree=prod_tree)
    if DEBUG: print('[INFO]: Finish calculating Product Tree Square')

    if DEBUG: print('[INFO]: Calculating Remainder Tree...')
    rem_tree = calc_rem_tree(prod=prod, prod_tree=prod_tree)
    if DEBUG: print('[INFO]: Finish Calculating Remainder Tree')

    if DEBUG: print('[INFO]: Calculating GCD...')
    moduli = cal_gcd(rem_tree=rem_tree, moduli_list=moduli_list)
    if DEBUG: print('[INFO]: Finish Calculating GCD')

    if DEBUG: print('[INFO]: Calculating Private Keys...')
    pvt_key = find_pvt_key(moduli=moduli)
    if DEBUG: print('[INFO]: Finish Calculating Private Keys')

    if DEBUG: print('[INFO]: Final Result...')
    get_result(pvt_key=pvt_key, cipher=cipher)

if __name__ == '__main__':
    main()