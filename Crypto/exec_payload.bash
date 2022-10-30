#! /usr/bin/env bash

COL1_FILE="col1"
COL2_FILE="col2"
PAYLOAD_SUFFIX_FILE="payload_suffix"
GOOD_FILE="sol_3.2.2_good.py"
EVIL_FILE="sol_3.2.2_evil.py"

printf "[INFO]: Append file %s to file %s...\n" $PAYLOAD_SUFFIX_FILE $COL1_FILE
cat $COL1_FILE $PAYLOAD_SUFFIX_FILE > $GOOD_FILE
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to cat files %s and %s to file %s. Quit.\n" $COL1_FILE $PAYLOAD_SUFFIX_FILE $GOOD_FILE
    exit $RETURN
fi
printf "[INFO]: Finish appending file %s to file %s\n" $PAYLOAD_SUFFIX_FILE $COL1_FILE
printf "[INFO]: Append file %s to file %s...\n" $PAYLOAD_SUFFIX_FILE $COL2_FILE
cat $COL2_FILE $PAYLOAD_SUFFIX_FILE > $EVIL_FILE
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to cat files %s and %s to file %s. Quit.\n" $COL2_FILE $PAYLOAD_SUFFIX_FILE $EVIL_FILE
    exit $RETURN
fi
printf "[INFO]: Finish appending file %s to file %s\n" $PAYLOAD_SUFFIX_FILE $COL2_FILE

printf "\n[INFO]: Check that %s and %s have the same MD5 Hash\n" $GOOD_FILE $EVIL_FILE
OPENSSL_MD5_GOOD_FILE=$(openssl dgst -md5 $GOOD_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute MD5(%s)\n" $GOOD_FILE
    exit $RETURN
fi
MD5_GOOD_FILE=$(cut -d " " -f 1 <<< $OPENSSL_MD5_GOOD_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute cut %s\n" $OPENSSL_MD5_GOOD_FILE
    exit $RETURN
fi
MD5_HASH_GOOD_FILE=$(cut -d " " -f 2 <<< $OPENSSL_MD5_GOOD_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute cut %s\n" $OPENSSL_MD5_GOOD_FILE
    exit $RETURN
fi
printf "[INFO]: %s %s\n" $MD5_GOOD_FILE $MD5_HASH_GOOD_FILE
OPENSSL_MD5_EVIL_FILE=$(openssl dgst -md5 $EVIL_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute MD5(%s)\n" $EVIL_FILE
    exit $RETURN
fi
MD5_EVIL_FILE=$(cut -d " " -f 1 <<< $OPENSSL_MD5_EVIL_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute cut %s\n" $OPENSSL_MD5_EVIL_FILE
    exit $RETURN
fi
MD5_HASH_EVIL_FILE=$(cut -d " " -f 2 <<< $OPENSSL_MD5_EVIL_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute cut %s\n" $OPENSSL_MD5_EVIL_FILE
    exit $RETURN
fi
printf "[INFO]: %s %s\n" $MD5_EVIL_FILE $MD5_HASH_EVIL_FILE
printf "[INFO]: Checking if the MD5 Hash are the same...\n"
if [ "$MD5_HASH_GOOD_FILE" != "$MD5_HASH_EVIL_FILE" ]
then
    printf "[ERROR]: The MD5 Hash of file %s and file %s are different. Quit.\n" $GOOD_FILE $EVIL_FILE
    exit 1
fi
printf "[INFO]: The MD5 Hash of file %s and file %s are the same\n" $GOOD_FILE $EVIL_FILE

printf "\n[INFO]: Check that %s and %s have different SHA256 Hash\n" $GOOD_FILE $EVIL_FILE
OPENSSL_SHA256_GOOD_FILE=$(openssl dgst -sha256 $GOOD_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute SHA256(%s)\n" $GOOD_FILE
    exit $RETURN
fi
SHA256_GOOD_FILE=$(cut -d " " -f 1 <<< $OPENSSL_SHA256_GOOD_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute cut %s\n" $OPENSSL_SHA256_GOOD_FILE
    exit $RETURN
fi
SHA256_HASH_GOOD_FILE=$(cut -d " " -f 2 <<< $OPENSSL_SHA256_GOOD_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute cut %s\n" $OPENSSL_SHA256_GOOD_FILE
    exit $RETURN
fi
printf "[INFO]: %s %s\n" $SHA256_GOOD_FILE $SHA256_HASH_GOOD_FILE
OPENSSL_SHA256_EVIL_FILE=$(openssl dgst -sha256 $EVIL_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute SHA256(%s)\n" $GOOD_FILE
    exit $RETURN
fi
SHA256_EVIL_FILE=$(cut -d " " -f 1 <<< $OPENSSL_SHA256_EVIL_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute cut %s\n" $OPENSSL_SHA256_EVIL_FILE
    exit $RETURN
fi
SHA256_HASH_EVIL_FILE=$(cut -d " " -f 2 <<< $OPENSSL_SHA256_EVIL_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute cut %s\n" $OPENSSL_SHA256_EVIL_FILE
    exit $RETURN
fi
printf "[INFO]: %s %s\n" $SHA256_EVIL_FILE $SHA256_HASH_EVIL_FILE
printf "[INFO]: Checking if the SHA256 Hash are different...\n"
if [ "$SHA256_HASH_GOOD_FILE" == "$SHA256_HASH_EVIL_FILE" ]
then
    printf "[ERROR]: The SHA256 Hash of file %s and file %s are different. Quit.\n" $GOOD_FILE $EVIL_FILE
    exit 1
fi
printf "[INFO]: The SHA256 Hash of file %s and file %s are different\n" $GOOD_FILE $EVIL_FILE

printf "\n[INFO]: Check that %s and %s generate different outputs\n" $GOOD_FILE $EVIL_FILE
printf "[INFO]: %s generate " $GOOD_FILE
python3 $GOOD_FILE
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute python script %s. Quit.\n" $GOOD_FILE
    exit $RETURN
fi
printf "[INFO]: %s generate " $EVIL_FILE
python3 $EVIL_FILE
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute python script %s. Quit.\n" $EVIL_FILE
    exit $RETURN
fi
printf "[INFO]: Checking if the outputs are different...\n"
RETURN=$(diff <(python3 $GOOD_FILE) <(python3 $EVIL_FILE))
if [ "$RETURN" == "" ]
then
    printf "[ERROR]: The outputs are the same. Quit.\n"
    exit $RETURN
fi
printf "[INFO]: The outputs are different\n"
