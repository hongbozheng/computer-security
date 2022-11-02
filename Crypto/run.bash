#! /usr/bin/env bash

GET_CERT_PREFIX="get_cert_prefix.py"
CERT_FILE="cert.cer"
CERT_PREFIX_FILE="cert_prefix"
FASTCOLL="fastcoll"
FASTCOLL_DIR="fastcoll_v1.0.0.5-1_source/"
MD5_1_FILE="md5_1"
MD5_2_FILE="md5_2"

printf "[INFO]: Get %s file from %s...\n" $CERT_PREFIX_FILE $CERT_FILE
./$GET_CERT_PREFIX $CERT_FILE $CERT_PREFIX_FILE $FASTCOLL_DIR$FASTCOLL $MD5_1_FILE $MD5_2_FILE
printf "[INFO]: Finish writing into %s file\n" $CERT_PREFIX_FILE