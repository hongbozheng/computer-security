#!/usr/bin/env python3
# CMD: ./sol_3.2.3.py 3.2.3_ciphertext.hex sol_3.2.3.txt

import sys
import urllib.request,urllib.error
from binascii import hexlify

BYTE_LEN=16
URL='http://172.22.159.75:8080/mp3/fa22_cs461_hongboz2/?'
DEBUG=1



def strip_padding(msg):
    padlen = 17 - ord(msg[-1])
    if padlen > 16 or padlen < 1:
        return True, None
    if msg[-padlen:] != ''.join(chr(i) for i in range(16,16-padlen,-1)):
        return True, None
    return False, msg[:-padlen]


# print(len(ciphertext))

# _, msg = strip_padding("".join(result))

def get_status(u):
    try:
        resp = urllib.request.urlopen(u)
        # if DEBUG: print(resp.read)
        return resp.code
    except urllib.error.HTTPError as e:
        # if DEBUG: print(e, e.code)
        return e.code

# Pad the message to a multiple of 16 bytes
def pad(msg):
    mod = len(msg)%BYTE_LEN
    return msg + ''.join(chr(i) for i in range(BYTE_LEN,mod,-1))

def main():
    if len(sys.argv) != 3:
        print('[USAGE]: ./sol_3.2.3.py <ciphertext.enc.asc> <decrypted_msg_file>')
        exit(1)

    with open(sys.argv[1]) as cipher_file:
        cipher = bytes.fromhex(cipher_file.read().strip())
    if DEBUG: print('[CIPHER]: %s'%cipher)
    exit()
    char_decrypted = []

    for pos in range(len(cipher) // 16 - 1, 0, -1):
        prev_cipher = cipher[16 * (pos - 1):16 * pos]
        current_block = cipher[16 * pos:16 * (pos + 1)]
        for offset in range(1, 17):
            target_byte = prev_cipher[-offset]
            # print(offset)
            for guess in range(256):
                prev_ciphertext[-offset] = guess
                if (guess != target_byte):
                    fake_cipher = hexlify(prev_ciphertext) + hexlify(current_block)
                    # print(fake_cipher)
                    url = URL + fake_cipher.decode()
                    # print(url)
                    status = get_status(url)

                    if status == 404:
                        # print(prev_ciphertext)
                        # print(guess, target_byte)
                        char_decrypted.append(chr(guess ^ 16 ^ target_byte))
                        print(chr(guess ^ 16 ^ target_byte))
                        for i in range(offset):
                            prev_ciphertext[-offset + i] = prev_ciphertext[-offset + i] ^ (16 - i) ^ (15 - i)  # remaining bytes of ct
                        break
                else:
                    guess = 0x10
                    fake_cipher = hexlify(prev_ciphertext) + hexlify(current_block)
                    # print(fake_cipher)
                    url = URL + fake_cipher.decode()
                    # print(url)
                    status = get_status(url)
                    # print(guess, target_byte)
                    if status == 404:
                        char_decrypted.append(chr(guess ^ 16 ^ target_byte))
                        print(chr(guess ^ 16 ^ target_byte))
                        for i in range(offset):
                            prev_ciphertext[-offset + i] = prev_ciphertext[-offset + i] ^ (16 - i) ^ (
                                        15 - i)  # remaining bytes of ct
                        break
    char_decrypted.reverse()
    print(char_decrypted)

if __name__ == '__main__':
    main()