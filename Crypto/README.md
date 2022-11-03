# MP3 - Crypto
##### Instructor: Adam Bates & Ling Ren
CP1 Deadline --- Tuesday, October 25th, 6:00PM

CP2 Deadline --- Thursday, November 3rd, 6:00PM

## Project Setup
1. Download VMWare
2. Download Ubuntu 18.04 LTS (CS461 Virtual Machine) at [here](https://uofi.box.com/s/aqaixm5igvqbyxys7gpswxgcsf7nyqo6)
3. Setup the VM in VMWare 

## Build Project
None

## Implementation
#### 3.1.1 Exercise
Type the following command to run the python script `3.1.1.py`
```
./3.1.1.py
```

#### 3.1.2 Substitute Cipher
Type the following command to run the python script `sol_3.1.2.py`
```
./sol_3.1.2.py 3.1.2_sub_ciphertext.txt 3.1.2_sub_key.txt sol_3.1.2.txt
```
or
```
python3 sol_3.1.2.py 3.1.2_sub_ciphertext.txt 3.1.2_sub_key.txt sol_3.1.2.txt
```
Change the `DEBUG` flag in the python script to `1` to print info to terminal

#### 3.1.3 AES: Decrypting AES
Type the following command to run the python script `sol_3.1.3.py`
```
./sol_3.1.3.py 3.1.3_aes_ciphertext.hex 3.1.3_aes_key.hex 3.1.3_aes_iv.hex sol_3.1.3.txt
```
or
```
python3 sol_3.1.3.py 3.1.3_aes_ciphertext.hex 3.1.3_aes_key.hex 3.1.3_aes_iv.hex sol_3.1.3.txt
```
Change the `DEBUG` flag in the python script to `1` to print info to terminal

#### 3.1.4 AES: Breaking A Weak AES Key
Type the following command to run the python script `3.1.4.py`
```
./3.1.4.py
```
or
```
python3 3.1.4.py
```

#### 3.1.5 Decrypting a ciphertext with RSA
Type the following command to run the python script `sol_3.1.5.py`
```
./sol_3.1.5.py 3.1.5_RSA_ciphertext.hex 3.1.5_RSA_private_key.hex 3.1.5_RSA_modulo.hex sol_3.1.5.hex
```
or
```
python3 sol_3.1.5.py 3.1.5_RSA_ciphertext.hex 3.1.5_RSA_private_key.hex 3.1.5_RSA_modulo.hex sol_3.1.5.hex
```
Change the `DEBUG` flag in the python script to `1` to print info to terminal

#### 3.1.6 Weak Hashing Algorithm
Type the following command to run the python script `sol_3.1.6.py`
```
./sol_3.1.6.py sol_3.1.6.txt sol_3.1.6.hex
```
or
```
python3 sol_3.1.6.py sol_3.1.6.txt sol_3.1.6.hex
```
Change the `DEBUG` flag in the python script to `1` to print info to terminal

#### 3.2.1 Length Extension
Type the following command to run the python script `sol_3.2.1.py`
```
python3 sol_3.2.1.py 3.2.1_query.txt 3.2.1_command3.txt sol_3.2.1.txt
```
Change the `DEBUG` flag in the python script to `1` to print info to terminal

#### 3.2.2 MD5 Collision
Run the following scripts
* get_sha256.bash
* exec_payload.bash

Type the following command to run the bash scripts
```
./get_sha256.bash
```
```
./exec_payload.bash
```

#### 3.2.3 Exploiting a Padding Oracle
Type the following command to run the python script `sol_3.2.3.py`
```
./sol_3.2.3.py 3.2.3_ciphertext.hex sol_3.2.3.txt
```
Change the `DEBUG` flag in the python script to `1` to print info to terminal

#### 3.2.4 Mining your Ps and Qs
Type the following command to run the python script `sol_3.2.4.py`
```
./sol_3.2.4.py 3.2.4_ciphertext.enc.asc moduli.hex sol_3.2.4.txt
```
Change the `DEBUG` flag in the python script to `1` to print info to terminal

#### 3.2.5 Creating Colliding Certificates
Type the following command to run the bash script `3.2.5.bash`
```
./3.2.5.bash
```
The bash script `3.2.5.bash` will run the python scripy below

or type the following command to run the python script `get_cert_col.py`
```
./get_cert_col.py cert.cer cert_DER.cer cer_prefix fastcoll_v1.0.0.5-1_source/fastcoll cert_col1 cert_col2 sol_3.2.5_certA.cer sol_3.2.5_certB.cer sol_3.2.5_factorsA.hex sol_3.2.5_factorsB.hex
```
Change the `DEBUG` flag in the python script to `1` to print info to terminal

## Developers
* Hongbo Zheng [NetID: hongboz2]
* Max Song [NetID: mcsong2]