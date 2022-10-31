#! /usr/bin/env bash

FASTCOLL="fastcoll"
FASTCOLL_DIR="fastcoll_v1.0.0.5-1_source/"
PREFIX_FILE="prefix"
COL1_FILE="col1"
COL2_FILE="col2"
SHA256_SUFFIX_FILE="sha256_suffix"
COL1_SHA256_FILE="col1_sha256.py"
COL2_SHA256_FILE="col2_sha256.py"
PAYLOAD_SUFFIX="payload_suffix"

printf "[INFO]: Using %s to generate 2 files with the same MD5 hash that both begin with %s\n" $FASTCOLL $PREFIX_FILE

printf "[INFO]: Executing %s...\n\n" $FASTCOLL
./$FASTCOLL_DIR$FASTCOLL -p $PREFIX_FILE -o $COL1_FILE $COL2_FILE
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute %s. Quit.\n" $FASTCOLL
    exit $RETURN
fi

printf "\n[INFO]: Append file %s to file %s...\n" $SHA256_SUFFIX_FILE $COL1_FILE
cat $COL1_FILE $SHA256_SUFFIX_FILE > $COL1_SHA256_FILE
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to cat files %s and %s to file %s. Quit.\n" $COL1_FILE $SHA256_SUFFIX_FILE $COL1_SHA256_FILE
    exit $RETURN
fi
printf "[INFO]: Finish appending file %s to file %s\n" $SHA256_SUFFIX_FILE $COL1_FILE
printf "[INFO]: Append file %s to file %s...\n" $SHA256_SUFFIX_FILE $COL2_FILE
cat $COL2_FILE $SHA256_SUFFIX_FILE > $COL2_SHA256_FILE
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to cat files %s and %s to file %s. Quit.\n" $COL2_FILE $SHA256_SUFFIX_FILE $COL2_SHA256_FILE
    exit $RETURN
fi
printf "[INFO]: Finish appending file %s to file %s\n" $SHA256_SUFFIX_FILE $COL2_FILE
printf "[INFO]: The 2 Python Scripts are %s and %s\n" $COL1_SHA256_FILE $COL2_SHA256_FILE

printf "\n[INFO]: Verify that %s and %s generate different SHA256 Hash\n" $COL1_SHA256_FILE $COL2_SHA256_FILE
COL1_SHA256=$(python3 $COL1_SHA256_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute python script %s. Quit.\n" $COL1_SHA256_FILE
    exit $RETURN
fi
printf "[INFO]: [%s] %s\n" $COL1_SHA256_FILE $COL1_SHA256
COL2_SHA256=$(python3 $COL2_SHA256_FILE)
RETURN=$?
if [ $RETURN -ne 0 ]
then
    printf "[ERROR]: Failed to execute python script %s. Quit.\n" $COL2_SHA256_FILE
    exit $RETURN
fi
printf "[INFO]: [%s] %s\n" $COL2_SHA256_FILE $COL2_SHA256
printf "[INFO]: Checking if 2 SHA256 Hash are different...\n"
if [ "$COL1_SHA256" == "$COL2_SHA256" ]
then
    printf "[ERROR]: The 2 SHA256 Hash are the same. Quit.\n"
    exit $RETURN
fi
printf "[INFO]: The 2 SHA256 Hash are different\n"