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
Change the `DEBUG` flag in the python script to `True` to print info to terminal

#### 3.1.3 AES: Decrypting AES
Type the following command to run the python script `sol_3.1.3.py`
```
./sol_3.1.3.py 3.1.3_aes_ciphertext.hex 3.1.3_aes_key.hex 3.1.3_aes_iv.hex sol_3.1.3.txt
```
or
```
python3 sol_3.1.3.py 3.1.3_aes_ciphertext.hex 3.1.3_aes_key.hex 3.1.3_aes_iv.hex sol_3.1.3.txt
```
Change the `DEBUG` flag in the python script to `True` to print info to terminal

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
Change the `DEBUG` flag in the python script to `True` to print info to terminal

#### 3.1.6 Weak Hashing Algorithm
Type the following command to run the python script `sol_3.1.6.py`
```
./sol_3.1.6.py 3.1.6_input_string.txt sol_3.1.6.hex
```
or
```
python3 sol_3.1.6.py 3.1.6_input_string.txt sol_3.1.6.hex
```
Change the `DEBUG` flag in the python script to `True` to print info to terminal

## Developers
* Hongbo Zheng [NetID: hongboz2]
* Max Song [NetID: mcsong2]