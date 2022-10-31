#!/usr/bin/env python3
# Command: python3 sol_3.2.1.py 3.2.1_query.txt 3.2.1_command3.txt sol_3.2.1.txt

import sys
import urllib.parse
from pymd5 import md5, padding

DEBUG=0

def main():
    if len(sys.argv) != 4:
        print('[USAGE]: python3 <your_script.py> <query_file> <command3_file> <output_file>')
        exit()

    with open(sys.argv[1], 'r') as query_file, open(sys.argv[2], 'r') as cmd_file:
        query = query_file.read().strip()
        cmd = cmd_file.read().strip()
        token = (query.split('&')[0]).split('=')[1]
        user = 'user=' + query.split('user=')[1]

    if DEBUG:
        print('[TOKEN]:         %s'%token)
        print('[USER]:          %s'%user)

    md5_hash = md5(state=token, count=512)
    md5_hash.update(cmd)
    if DEBUG:
        print('[CMD_MD5_HASH]:  %s'%md5_hash.hexdigest())
        print('[PADDING_BYTE]:  %s'%padding((len(user)+8)*8))
        print('[NEW_QUERY]:     '+'token='+md5_hash.hexdigest()+'&'+user+urllib.parse.quote_from_bytes(bs=padding((len(user)+8)*8),safe='/')+cmd)

    with open(sys.argv[3], 'w') as out:
        out.write('token='+md5_hash.hexdigest()+'&'+user+urllib.parse.quote_from_bytes(bs=padding((len(user)+8)*8),safe='/')+cmd)

if __name__ == '__main__':
    main()