#!/usr/bin/env python3
# -*- coding: latin-1 -*-

from hashlib import sha256

BENIGN_PAYLOAD='I come in peace.'
MALICIOUS_PAYLOAD='Prepare to be destroyed!'
blob="""
                          ǧ�vSZ>nS�e���'�6��"M��!����������@�=��_�&�Y���;;)�H?�)(_^�~��͗�h ���w�X�[��LaYQSV��Vsi���p�����W��][��!�
"""

if sha256(blob.encode(encoding='UTF-8',errors='strict')).hexdigest() == '51fc54dba1dac9edbd2528b2e0a321a42d3afabe76a872b39009a58a2f570032':
    print(BENIGN_PAYLOAD)
else:
    print(MALICIOUS_PAYLOAD)