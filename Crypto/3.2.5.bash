#! /usr/bin/env bash

GET_CERT_COL="get_cert_col.py"
CERT_FILE="cert.cer"
CERT_DER_FILE="cert_DER.cer"
CERT_PREFIX_FILE="cert_prefix"
FASTCOLL="fastcoll"
FASTCOLL_DIR="fastcoll_v1.0.0.5-1_source/"
CERT_COL1_FILE="cert_col1"
CERT_COL2_FILE="cert_col2"
CERT_A_FILE="sol_3.2.5_certA.cer"
CERT_B_FILE="sol_3.2.5_certB.cer"
FACTOR_A_FILE="sol_3.2.5_factorsA.hex"
FACTOR_B_FILE="sol_3.2.5_factorsB.hex"

printf "[INFO]:     Starting MAGIC script...\n"
./$GET_CERT_COL $CERT_FILE $CERT_DER_FILE $CERT_PREFIX_FILE $FASTCOLL_DIR$FASTCOLL $CERT_COL1_FILE $CERT_COL2_FILE $CERT_A_FILE $CERT_B_FILE $FACTOR_A_FILE $FACTOR_B_FILE
printf "[INFO]: Finish executing MAGIC script\n"
