#!/usr/bin/env python3
# CMD: ./sol_3.2.3.py 3.2.3_ciphertext.hex sol_3.2.3.txt

import sys
import urllib.request,urllib.error

HEX_16=0x10
URL='http://172.22.159.75:8080/mp3/fa22_cs461_hongboz2/?'
DEBUG=1

def get_status(u):
    try:
        resp = urllib.request.urlopen(u)
        return resp.code
    except urllib.error.HTTPError as e:
        # if DEBUG: print(e, e.code)
        return e.code

def get_plaintxt(decrypted_char):
    decrypted_char.reverse()
    pad_num = len(decrypted_char)%HEX_16
    if pad_num == 0:
        pad_num = HEX_16
    for i in range(pad_num):
        del decrypted_char[-1]
    return ''.join(decrypted_char)

def main():
    if len(sys.argv) != 3:
        print('[USAGE]: ./sol_3.2.3.py <ciphertext.enc.asc> <decrypted_msg_file>')
        exit(1)

    with open(sys.argv[1]) as ciphertxt_hex_file:
        ciphertxt_byte = bytearray(bytes.fromhex(ciphertxt_hex_file.read().strip()))
    if DEBUG: print('[CIPHERTXT_BYTE]: %s\n'%bytes(ciphertxt_byte))

    decrypted_char = []

    if DEBUG: print('[INFO]: Start Decryption...')
    for pos in range(len(ciphertxt_byte)//HEX_16-1, 0, -1):
        ciphertxt_byte_prev = ciphertxt_byte[16*(pos-1):16*pos]
        cur_blk = ciphertxt_byte[HEX_16*pos:HEX_16*(pos+1)]
        for offset in range(1, HEX_16+1):
            target_byte = ciphertxt_byte_prev[-offset]
            for guess in range(256):
                ciphertxt_byte_prev[-offset] = guess
                if (guess != target_byte):
                    fake_cipher = ciphertxt_byte_prev.hex() + cur_blk.hex()
                    url = URL + fake_cipher
                    status = get_status(url)

                    if status == 404:
                        decrypted_char.append(chr(target_byte^guess^HEX_16))
                        if DEBUG: print('[CHAR]: %c'%chr(target_byte^guess^HEX_16))
                        for i in range(offset):
                            ciphertxt_byte_prev[-offset+i] = ciphertxt_byte_prev[-offset+i]^(HEX_16-i)^(HEX_16-1-i)
                        break
                else:
                    guess = 0x10
                    fake_cipher = ciphertxt_byte_prev.hex() + cur_blk.hex()
                    url = URL + fake_cipher
                    status = get_status(url)

                    if status == 404:
                        decrypted_char.append(chr(target_byte^guess^HEX_16))
                        if DEBUG: print('[CHAR]: %c'%chr(target_byte^guess^HEX_16))
                        for i in range(offset):
                            ciphertxt_byte_prev[-offset+i] = ciphertxt_byte_prev[-offset+i]^(HEX_16-i)^(HEX_16-1-i)
                        break

    if DEBUG: print('[INFO]: Finish Decryption')
    plaintxt = get_plaintxt(decrypted_char=decrypted_char)
    if DEBUG: print('[PLAINTXT]: %s'%plaintxt)

    with open(sys.argv[2], 'w') as decrypted_msg_file:
        decrypted_msg_file.write(plaintxt)

if __name__ == '__main__':
    main()