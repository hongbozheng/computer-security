#! /usr/bin/env bash

GET_CERT_COL="get_cert_col.py"
CERT_FILE="cert.cer"
CERT_PREFIX_FILE="cert_prefix"
FASTCOLL="fastcoll"
FASTCOLL_DIR="fastcoll_v1.0.0.5-1_source/"
CERT_COL1_FILE="cert_col1"
CERT_COL2_FILE="cert_col2"

printf "[INFO]: Get %s file from %s...\n" $CERT_PREFIX_FILE $CERT_FILE
./$GET_CERT_COL $CERT_FILE $CERT_PREFIX_FILE $FASTCOLL_DIR$FASTCOLL $CERT_COL1_FILE $CERT_COL2_FILE
printf "[INFO]: Finish writing into %s file\n" $CERT_PREFIX_FILE
