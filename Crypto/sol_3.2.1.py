#!/usr/bin/env python3
# Command: python3 sol_3.2.1.py 3.2.1_query.txt 3.2.1_command3.txt sol_3.2.1.txt

import sys
import urllib.parse
from pymd5 import md5, padding

DEBUG=1

def main():
    if len(sys.argv) != 4:
        print('[USAGE]: python3 <your_script.py> <query_file> <command3_file> <output_file>')
        exit(1)

    with open(sys.argv[1], 'r') as query_file, open(sys.argv[2], 'r') as cmd3_file:
        query = query_file.read().strip()
        cmd3 = cmd3_file.read().strip()
    token = (query.split(sep='&', maxsplit=1)[0]).split(sep='=')[1]
    usr_cmd1_cmd2 = query.split(sep='&', maxsplit=1)[1]

    if DEBUG:
        print('[QUERY]:         %s'%query)
        print('[TOKEN]:         %s'%token)
        print('[USR_CMD1_CMD2]: %s'%usr_cmd1_cmd2)
        print('[CMD3]:          %s'%cmd3)

    pad_byte = padding((len(usr_cmd1_cmd2)+8)*8)
    md5_hash = md5(state=token, count=512)
    md5_hash.update(cmd3)

    if DEBUG:
        print('[CMD_MD5_HASH]:  %s'%md5_hash.hexdigest())
        print('[PADDING_BYTE]:  %s'%pad_byte)
        print('[NEW_QUERY]:     %s'%('token='+md5_hash.hexdigest()+'&'+usr_cmd1_cmd2+urllib.parse.quote_from_bytes(bs=pad_byte,safe='/')+cmd3))

    with open(sys.argv[3], 'w') as out:
        out.write('token='+md5_hash.hexdigest()+'&'+usr_cmd1_cmd2+urllib.parse.quote_from_bytes(bs=pad_byte,safe='/')+cmd3)

if __name__ == '__main__':
    main()