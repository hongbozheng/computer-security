import urllib.request, urllib.error
from binascii import hexlify

def get_status(u):
    try:
        resp = urllib.request.urlopen(u)
        return resp.code
    except urllib.error.HTTPError as e:
        return e.code


# Pad the message to a multiple of 16 bytes
def pad(msg):
    n = len(msg)%16
    return msg + ''.join(chr(i) for i in range(16,n,-1))


def strip_padding(msg):
    padlen = 17 - ord(msg[-1])
    if padlen > 16 or padlen < 1:
        return True, None
    if msg[-padlen:] != ''.join(chr(i) for i in range(16,16-padlen,-1)):
        return True, None
    return False, msg[:-padlen]


with open("3.2.3_ciphertext.hex") as f:
    ciphertext = bytearray(bytes.fromhex(f.read().strip()))
print(ciphertext)
# print(len(ciphertext))

base_url = "http://172.22.159.75:8080/mp3/fa22_cs461_mcsong2/?"
result = []

for pos in range(len(ciphertext) // 16 - 1, 0, -1):
    prev_ciphertext = ciphertext[16 * (pos - 1):16 * pos]
    current_block = ciphertext[16 * pos:16 * (pos + 1)]
    for offset in range(1, 17):
        target_byte = prev_ciphertext[-offset]
        # print(offset)
        for guess in range(256):
            prev_ciphertext[-offset] = guess # 
            if(guess != target_byte):
                fake_cipher = hexlify(prev_ciphertext) + hexlify(current_block)
                # print(fake_cipher)
                url = base_url + fake_cipher.decode()
                # print(url)
                status = get_status(url)
                
                if status == 404:
                    # print(prev_ciphertext)
                    # print(guess, target_byte)
                    result.append(chr(guess ^ 16 ^ target_byte))
                    print(chr(guess ^ 16 ^ target_byte))
                    for i in range(offset):
                        prev_ciphertext[-offset + i] = prev_ciphertext[-offset + i] ^ (16 - i) ^ (15 - i) # remaining bytes of ct 
                    break
            else:
                guess = 0x10
                fake_cipher = hexlify(prev_ciphertext) + hexlify(current_block)
                # print(fake_cipher)
                url = base_url + fake_cipher.decode()
                # print(url)
                status = get_status(url)
                # print(guess, target_byte)
                if status == 404:
                    result.append(chr(guess ^ 16 ^ target_byte))
                    print(chr(guess ^ 16 ^ target_byte))
                    for i in range(offset):
                        prev_ciphertext[-offset + i] = prev_ciphertext[-offset + i] ^ (16 - i) ^ (15 - i) # remaining bytes of ct 
                    break


result.reverse()
# _, msg = strip_padding("".join(result))
print(result) 