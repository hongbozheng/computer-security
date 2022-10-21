#!/usr/bin/env python3

from Crypto.Cipher import AES

AES_WEAK_CIPHERTEXT='3.1.4_aes_weak_ciphertext.hex'
KEY_BIT=256
BITS=KEY_BIT-251

def main():
    iv_byte = bytes.fromhex('%032X'%0)
    with open(AES_WEAK_CIPHERTEXT, 'r') as cipher:
        cipher_byte = bytes.fromhex(cipher.read().strip())

    for i in range(2**BITS):
        key = '%064X'%i
        key_byte = bytes.fromhex(key)
        print('[KEY]:         %s'%key)
        print('[KEY_BYTE]:    %s'%key_byte)
        print('[IV_BYTE]:     %s'%iv_byte)
        print('[CIPHER_BYTE]: %s'%cipher_byte)
        aes = AES.new(key=key_byte, mode=AES.MODE_CBC, iv=iv_byte)
        try:
            print('[DECRYPT]:     %s'%aes.decrypt(cipher_byte).decode(encoding='UTF-8', errors='strict'))
        except:
            pass
        print('--------------------------------------------------------------------------------------------------------'
              '------------------------------------------')
if __name__ == '__main__':
    main()