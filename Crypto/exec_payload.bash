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
