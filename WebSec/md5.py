#!/usr/bin/env python3

import hashlib

NetID = 'hongboz2'

def main():
    m = hashlib.md5()
    m.update(NetID.encode('UTF-8'))
    print(m.digest().hex())

if __name__ == '__main__':
    main()
