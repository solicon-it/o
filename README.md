# A Python commandline to handle your Oracle Landscape

Currently we see the Python commandline as an extension to our ORAtk framework which
exists inside databases and as sqlplus-scripts in combination with a customized environment.
As a consequence there are some dependencies to enviroment-settings. This is mainly for
convenience! But this program also works in "stand alone" mode without using ORAtk parts.


## An (incomplete) Featurelist

### Currently available

* Configure your database landscape once and access all your database with minimum effort.
* Execute common DBA commands (e.g. looking uper users, datafile, tablespaces, block, ...)
* Execute custom SQL-statements (via cmdline or file).
* Gather data from multiple databases with just one command in parallel (default) or serial mode.
* Print resultsets nicely formatted.


### Planned
* Save a resultset back into some (Oracle) database.


## Parallel processing
Per default parallel processing is always enabled when applying some command to multiple
databases. Max 16 workers are spawned (or less, if your list of databases is shorter.)
This value (max. degree of parallelism) can be adjusted when using the --parallel flag.

It is possible to switch to serial processing when using the --serial flag.


## Identifying databases

Basically there are these options:

1. Provide the database as commandline parameter (-d / --db | --cdb | --pdb)
   Using --cdb or --pdb also applies an additional filter as only databases with a
   matching type are take into consideration. (See file "databases.py")

2. Derive the database from your current ORAtk-setting
   Environment variable $DBA_DB_NAME is evaluated in this case.


### Accessing multiple databases at once

It is possible to use additional modifiers in combination with the --db paramater:

1. You can manually define multiple databases
   E.g. --db DB1 DB2 DB3 ... this works only, if these dbs are defined inside "databases.py".

2. You can also use all databases
   Just use: --db all or --pdb all or --cdb all (--pdb/--cdb act as implicit filters!)

3. Using tags you can easily create lists of "interesting" databases
   E.g. --db all --tag TEST ... I am only interested in databases with tag "TEST"


## Identifying users and passwords

This process involves two separate, but connected (at least regarding used datastructures)
steps.

### Set / get the user

We have different paths to define the Oracle username. The rules to identify an user
are applied in the given order.

1. Provide the user as commandline parameter (-u / --usr).
   The easiest ond most flexible option. You can use this approach for doing "adhoc"
   operations with some special user, without doing any addional configuration in file
   "databases.py".

2. Use your current username at os level.
   This utilizes the idea of minimal configuration and still uses personalized logins.
   But it can only work, if your database-user matches your os-user. (This has nothing
   to do with "External Authentication" as it is mentioned in the Oracle documentation.)

3. Use the DEFAULT_USER defined in file "databases.py".
   Inside this file you define users and databases. "DEFAULT_USER" can be used as a
   shortcut for your most common Oracle user in your database landscape.

4. Extract the user from ORAtk environment variables.
   Based on your current DB-environment, a sqlplus login-file may exist in directory
   $HOME/sqlplus-logins.


### Finding the correct password for an user

After we selected the appropriate user, we still need to find a password for this user.
Otherwise we won't be able to login into the database. Similar as with usernames there
are also some options how to select a password.

1. Provide the user as commandline parameter (-p / --pwd).
   See option 1 in the previous section. This is just the logical consequence of
   being able to provide an Oracle username.

2. Lookup for a password provided in file "databases.py"
   You can define multiple passwords for each user. Each password may be valid for one
   or more databases. At this stage you already know the database and the user, so it is
   quite easy to come up with a password if it is configured.

3. Extract the password from some sqlplus login-file
   This is some kind of fallback and matches option 3 in the previous section.

If none of these paths lead to a password for your choosen user and database, we stop
here with some error-message.


## Configure your database landscape

Configuration happens inside a the Python file `o/cfg/databases.py`. So your configuraion is just
ordinary Python code! Pls be aware that this file shall NEVER be committed back into our bitbucket
repository. So a little bit of Python knowledge will be helpful, but it is not that complicated!
In the end it is totally up to you how to set this up for your location.

Some conventions regarding configuration (Python is case sensitive!):

* Database-variables MUST be uppercase
* User-variables MUST be uppercase
* TAG defintions (can be attached to databases for some advanced filtering) MUST be uppercase

All rules when coding Python apply also! So if you have some typo in your configuration, you will get
a Python runtime error, complaining about something ... ;)


### Configure Databases

This happens by instantiating a database object. An example:
```python
KB = ora.database(name='KB', host='vm002',  tns='kb', type='PDB', version=_v)
CDB1 = ora.database(name='CDB1', host='vm002', service_name='cdb1.zuhause', type='CDB', port=1521, version='19.9.0')
CDB1.pdbs = [KB]
```
Basically you are introducing 2 new variables (KB, CDB1) as Oracle database objects containing some properties
and we relate these 2 databases by adding KB to the pdb-list of CDB1.

Property 'name' can be used as an shortcut for service-name. It is just a name for your database variable when
you print it (e.g. `o list -d all`).
When emitting data from multiple databases 'name' is also shown in column '_db'.

Properties 'host', 'service_name' and 'port' are necessary to identify a database. Type-information (CDP / PDB / CLASSIC)
is used for additional filtering at the commandline (e.g. --pdb automatically enforces to use only databases with type 'PDB').

Property 'tns' can be used alternatively when you work with "tnsnames.ora". In this case 'tns' describes the
name of some entry inside file "tnsnames.ora".

Property 'rac' is used to disdinguish between a cluster-service (any database instance of the cluster can be
elected by Oracle to fulfill your request) or an instance on a specific node (SINGLE-NODE) when you work with
Oracle Real Application Clusters. For normal databases 'rac' = None.
This flag is also important to filter database instances when adressing multiple databases with modifier "all".
It guarantees not to use multiple instances of the same cluster when gathering data.

Property 'version' is planned for fine-tuning some behaviour when executing various commands.
Currently it is not in use, so it is just some additional information.

Property 'tags' can be used to mark databases. So you can group databases together regarding some aspect.
(E.g. PROD, TEST, DEV or some Application, ...) You can define multiple tags per database. Currently tags are
just a simple list.
**Attention! Tags must always be entered in uppercase!**

How to organize the list of databases is up to you. Just the usual restrictions when coding in Python apply here!


## Configure Users

User configuration happens after all databases have been defined. Users and databases have a one to many relationship.
It is quite common to share an usera account across many databases. Here is an example:
```python
DBADMIN = ora.user(name = 'DBADMIN', sysdba = False)
DBADMIN.set_pwd('fernet:gAAAAABgzbCb_oD5csT_6mkLTTMNbsGfkPARE2yYriSPc43PbcfUEVR2pwxDkz48MVg8E8Nvt-BMdTg4JXhVcBxdkBOlpqoW5w==',
                [KB, KB_Q])
```
User DBADMIN is defined with name "DBADMIN" (this name is used for login into the database) and does
not have SYSDBA privileges. (Logging in as SYSDBA is different from a normal login opertation.)
We defined 1 password (encrypted) for this user, which is used to login into database KB and KB_Q.
The list of databases is not limited! Maybe you use the same password for 20 databases.

But may you have different passwords for the same user on different databases. In this situation you
just add mutiple "set_pwd"-calls. E.g.:
```python
DBADMIN = ora.user(name = 'DBADMIN', sysdba = False)
DBADMIN.set_pwd('fernet:gAAAAABgzbCb_oD5csT_6mkLTTMNbsGfkPARE2yYriSPc43PbcfUEVR2pwxDkz48MVg8E8Nvt-BMdTg4JXhVcBxdkBOlpqoW5w==',
                [KB_Q])
DBADMIN.set_pwd('dbadmin', [KB])
```
We use 2 different passwords for user DBADMIN on databases KB and KB_Q. For database KB the password is not even encrypted!


## Configure a default User

As DBA's are super lazy (at least I am), you can define a user that shall be used always to access a database
whenever no user was provided at the commandline.

You just set the variable DEFAULT_USER to some user.
```python
DEFAULT_USER = DBADMIN
```

If you do not want to use a default user, than unset this variable:
```python
DEFAULT_USER = None
```


## Managing Passwords

Having passwords prepared in some configuration file so you do not need to retype them all the
time is a "must have" feature regarding convenience. On the other hand storing passwords
unencrypted on some workstation is an absolutly NO GO for any security officer!

To have it both (security & convenience) passwords in file 'databases.py' can be encrypted.
Symmetric-key Encryption (Fernet) is used for this job. (See python library "cryptography" for
further details.)

When working with encrypted passwords you need to generate a key and keep it safe in some
password store! Otherwise there is no way to decrypt your passwords again!

As an alternative you can rely on Oracle wallets to handle passwords. In this case you have to
configure your sqlnet/tnsnames setup. (Details are further down.)


### Generate an enycryption key

This can also be done directly from the commandline:
```bash
o genkay
Set environment variable ORACMD_KEY to use this key for encrypting passwords.

KEY = 8fH88XNdgiIDBFLccu3RKl0aFNU17uZzCbs2Flce6RM=

... and keep it separatly in some password-manager, otherwise will NOT be able to decrypt your passwords in file 'databases.py'!
```
The provided key is just an example! It is essential to find some save place for this key!
(As mentioned - some kind of password safe is fine.)

To use this key for encrypting and decrypting password, you need to set it in your environment.
The variable name is "ORACMD_KEY". So this is still not perfectly secure, but it is way better
than having files lying around with DBA logins for your production databases!

```bash
export ORACMD_KEY=8fH88XNdgiIDBFLccu3RKl0aFNU17uZzCbs2Flce6RM
```

If you set this up (and stored the key somewhere!), you can continue with encrypting your passwords.
DO NOT STORE THIS KEY IN SOME ENVIRONMENT FILE (e.g. ".bash_profile" or similar) !!!

### Encrypt passwords

Also a simple operation from the commandline:
```bash
o encrypt -p some_password
Encrypted pwd = fernet:gAAAAABgzbzi9Wga64TbjuOWV4lkaReA4VuLO3EGABHCyARbNMsNVMroKy0RioeaGjfZyUKVB6LaP6UsFRU9wQ6UM8uRSkPO-g==
```

As a next step you just copy the encrypted password (prefix "fernet:" is important otherwise decryption will not happen!)
and replace the existing plaintext password in file 'databases.py'. Save this file and you are ready to go!


### Decrypt passwords

This will happen automatically whenever the program recognises an encrypted password. (This is why prefix "fernet:" is
necessary when using encryption.) Currently I see no need to provide an extra "decrypt" command. So this feature is
not implemented.


### Using Oracle wallets
If you don't trust the described encryption strategy for passwords from above, you can switch to Oracle wallets instead.
You need to:
* Create an Oracle wallet and add TNS-Name / User / Password information.
* Add tnsnames entries for each User / Database combination you want to use.
* Add the wallet setup to your sqlnet.ora file

An example:
```bash
cd $ORACLE_HOME/network/admin
mkstore -wrl . -create

# Add the credentials for DBADMIN@DBADMIN_KB (DBADMIN_KB must be added to your tnsnames.ora)
mkstore -wrl . -createCredential DBADMIN_KB DBADMIN <Pwd of DBADMIN>

# Modify file sqlnet.ora
WALLET_LOCATION = (SOURCE= (METHOD=FILE) (METHOD_DATA= (DIRECTORY="<ORA-HOME>/network/admin")))
SQLNET.WALLET_OVERRIDE = TRUE

# Do not forget to adjust file permissions for the generated wallet files! Otherwise access for
# users other than "oracle" may fail.
```

Frank Pachot explains this in https://franckpachot.medium.com/passwordless-data-pump-19c-b21cd1e00c16 quite detailed.
AskTom mentions some options when you need multiple users set up like this inside one database:
https://asktom.oracle.com/pls/apex/asktom.search?tag=multiple-schema-oracle-wallet

Pros are:
* It may be easier to trust Oracle wallet technology instead of some third party source with an "unknow"
  encryption implementation.

Cons are:
* Additional configuration on Oracle side (tnsnames.ora can get quite large. You need a separate tns-entry for
  each User / database combination.)
* Configuration in "databases.py" gets also bigger. (You need to define the mapping between user / database / tns-entry
  for each combination.)

A configuration example:
```python
DBADMIN = ora.user(name = 'DBADMIN', sysdba = False)
DBADMIN.set_wallet(tns='DBADMIN_KB', db=KB)
```


## Using custom queries

With command "query" you can use your own sql-statements and scripts in addition to the already predefined commands.
"query" may be used together with the flags --sql or --file.


### Using flag -s / --sql

For short sql-statements this is quite convenient:
```bash
o query -s "select count(*) from dba_objects where owner='DBADMIN'" --pdb all

    | _db   |   COUNT(*)
----+-------+------------
  0 | KB    |         74
  0 | KB_Q  |         18

```

Be aware the single and double quotes are handled (and interpreted!) by the Linux commandline here. If you are using
double quotes some special characters (e.g. "$") are handled differently!

```bash
o query -s "select count(*) from v$session where username='DBADMIN'" --pdb all
error executing command for database 'None' - processing stopped!
error message is: Execution failed on sql 'select count(*) from v where username='DBADMIN'': ORA-00942: table or view does not exist
```

V$SESSION is interpreted by bash as "V" concatinated with the (non existing) variable $SESSION, which results in
the error message above.

If you have no string-comparisons in your sql-stmt, you just can use single quotes:

```bash
o query -s 'select count(*) from v$session' --pdb all
    | _db   |   COUNT(*)
----+-------+------------
  0 | KB    |         59
  0 | KB_Q  |         51
```

otherwise you need to escape the character "$":

```bash
o query -s "select count(*) from v\$session where username='DBADMIN'" --pdb all
    | _db   |   COUNT(*)
----+-------+------------
  0 | KB    |          5
  0 | KB_Q  |          1
```

Although flag --sql provides a lot of additional flexibility, it is not efficient using this flag for longer sql-statements.
Typing and "debugging" gets quite nasty!


### Using flag --file

With this flag you can use any sql-statement stored in some file. If you put your scripts inside sub-directory "scripts"
(located in the base directory of "o"), you can use the filename directly. Otherwise you need to provide the fully
qualified path and filename.

If sub-directory "scripts" is not feasable in your environment, you can adjust variable "_SQL_SCRIPT_DIR" inside config-file
"databases.py" to use some custom location for your sql-scripts.

An example (using a filename only):

```bash
o query --file fra_usage_pct.sql --cdb all -u sys

    | _db   | DISPLAY_VALUE   |   ARCHIVELOGS |   BACKUPS |   IMAGE_COPIES |   FLASHBACK_LOGS |   OTHER |   TOTAL
----+-------+-----------------+---------------+-----------+----------------+------------------+---------+---------
  0 | CDB1  | 8G              |         13.28 |      1.35 |              0 |                0 |       0 |   14.63
  0 | CDB2  | 0               |        nan    |    nan    |                |                  |         |  nan
```

You can even apply a custom filter ("-f2") and sort expressions ("-o"):
```bash
o query --file fra_usage_pct.sql --cdb all -u sys -f2 "total > 30"
    | _db   | RECO_DEST_SIZE   |   ARCHIVELOGS |   BACKUPS |   IMAGE_COPIES |   FLASHBACK_LOGS |   OTHER |   TOTAL
----+-------+------------------+---------------+-----------+----------------+------------------+---------+---------
  0 | CDB1  | 8G               |         38.17 |      1.57 |              0 |                0 |       0 |   39.74
```

But this is only working, if you organize your SQL-statement to have a simple SELECT in the main part without
any WHERE predicates or ORDER BY expressions. "o" just appends additional WHERE-conditions and/or ORDER BY
expressions at the end of your SQL-statements (Any ";" is removed upfront.)
Simple filters "(-f") do not work!

**Currently "o" can only process sql-scripts that contain exactly 1 sql-statment.**

Files containing multiple sql-statements or PL/SQL-blocks are not supported yet.


## Executing DDL statements
DDL statements are also queries (but are handled differently regarding predicates and sorting). So the command here
is also "query". To mark a statement as DDL operations flag "--ddl" (or "-D" as shortcut) must be provided also!
The result of a DDL operation is always a table containing the DDL-statement and the result per database.

An example:
```bash
o query -s "grant select on dba_objects to dbadmin" --pdb kb kb_q -u sys -D
    | _db   | DDL-Stmt                                | Result
----+-------+-----------------------------------------+----------
  0 | KB    | grant select on dba_objects to dbadmin; | OK
  0 | KB_Q  | grant select on dba_objects to dbadmin; | OK
```

Another example (DDL fails on one database):
```bash
o query -s "alter user kurt account lock" --pdb kb kb_q -u sys --ddl
    | _db   | DDL-Stmt                      | Result
----+-------+-------------------------------+---------------------------------------
  0 | KB    | alter user kurt account lock; | OK
  0 | KB_Q  | alter user kurt account lock; | ORA-01918: user 'KURT' does not exist
```

If you forget the flag "--ddl" and "o" recognizes a DDL statment, you get an error message informing you about this:
```bash
o query -s "drop table t1 purge" --pdb all -u dbadmin
This seems to be a DDL-statement (DROP ...). Use flag --ddl / -D here!
```


### Invoking DDL-scripts

You can put your DDL-statement also into a file. E.g. some CREATE TABLE statement:
```sql
create table dbadmin.t1(
  id number(10) not null
 ,code varchar2(10)
 ,constraint t1_pk primary key (id)
);
```

We save this DDL-statement into file t1.sql (inside the current directory) and execute it:
```bash
o query --file ./t1.sql --pdb all -u dbadmin -D
    | _db   | DDL-Stmt                            | Result
----+-------+-------------------------------------+----------
  0 | KB    | create table dbadmin.t1(            | OK
    |       |   id number(10) not null            |
    |       |  ,code varchar2(10)                 |
    |       |  ,constraint t1_pk primary key (id) |
    |       | );                                  |
  0 | KB_Q  | create table dbadmin.t1(            | OK
    |       |   id number(10) not null            |
    |       |  ,code varchar2(10)                 |
    |       |  ,constraint t1_pk primary key (id) |
    |       | );                                  |
```

Note: We provided the name of our SQL-script qualified (using "./")! The is necessary because this file is not
inside the default script directory.

**ATTENTION**
Currently there are some restrictions:
- "o" cannot handle scripts with multiple DDL-statements inside!
- SQL-scripts are not checked regarding DDL-statements. (You will get a runtime error!)


## List configuration details

Currently the LIST command can show information about databases and files inside SCRIPT_DIR.


### List database details

You can use this command to get a quick overview about which databases are configured inside file "databases.py".
All flags to filter / adjust the database list work here also.

```bash
o list --db all
    | name   | type   | version   | tns   | service      | host   | rac   | tags
----+--------+--------+-----------+-------+--------------+--------+-------+--------
  0 | CDB1   | CDB    | 19.9.0    |       | cdb1.zuhause | vm002  |       | []
  1 | CDB2   | CDB    | 19.9.0    |       | cdb2.zuhause | vm002  |       | []
  2 | KB     | PDB    | 19.9.0    | kb    |              | vm002  |       | []
  3 | KB_Q   | PDB    | 19.9.0    |       | kb_q.zuhause | vm002  |       | ['Q']
```

E.g. filter by some tag:
```bash
o list --db all --tag Q
    | name   | type   | version   | tns   | service      | host   | rac   | tags
----+--------+--------+-----------+-------+--------------+--------+-------+--------
  0 | KB_Q   | PDB    | 19.9.0    |       | kb_q.zuhause | vm002  |       | ['Q']
```


### List script details

Use this command to get information about available files inside your configured SCRIPT_DIR.

```bash
o list --file all
 name              | status    | type     | description
-------------------+-----------+----------+-----------------------------------------------------------------------------------
 fra_usage_pct.sql | VALID     | SQL-STMT | The current size of the fast-recovery-area and some usage information in percent.
 xx.sql            | NO-CONFIG |          |
```

So file "fra_usage_pct.sql" is VALID and we can also provide some additional information. File "xx.sql" only exists on the
filesystem inside directory SCRIPT_DIR. It can be used, but we have no additional metadata about it.

**About file "scripts.csv":**
This file also exists inside directory SCRIPT_DIR. It is a CSV-file with (currently) 3 columns and has to be maintained manually.

```bash
cat scripts.csv
"name","type","description"
"fra_usage_pct.sql","SQL-STMT","The current size of the fast-recovery-area and some usage information in percent."
```

If you have many files you can filter by filename (regex). Instead of using "all" you can define any regex.
(Regex filtering happens case insensitive.)

```bash
o list --file f
 name              | status   | type     | description
-------------------+----------+----------+-----------------------------------------------------------------------------------
 fra_usage_pct.sql | VALID    | SQL-STMT | The current size of the fast-recovery-area and some usage information in percent.
```

## Save results
Per default results are always displayed in your terminal window. With flag "--save" you decide where to save results.

### Save results into files
To save data we can choose between those formats:
* csv
* html
* parquet (binary format - often used in bigdata setups)
* xslx (Excel 2003 or later)

The output format is identified by the extension of the file you define after flag "--save".

An example:
```bash
o df --pdb kb kbo df --pdb kb kb_q -u dbadmin --save users.xlsx
File 'users.xlsx' created (6 kb).
```

A remark:
Creating "xslx" files can take quite long! If you save bigger resultsets CSV of PARQUET are good options.


## Some remarks about commands in general

TDB ...


## Currently implemented commands

### blocks
Find currently blocking sessions.

Example:
```bash
o blocks -u sys
    | _db   |   INST_ID | SESSIONINFO   |   SPID | USERNAME   | OSUSER   | MACHINE       | STATUS   |   LAST_CALL_ET | EVENT                         | WAITING_FOR
----+-------+-----------+---------------+--------+------------+----------+---------------+----------+----------------+-------------------------------+---------------
  0 | KB    |         1 | 603,25133,@1  |  54346 | DBADMIN    | kurt     | vm002.zuhause | INACTIVE |             46 | SQL*Net message from client   |
  1 | KB    |         1 | ..18,42926,@1 |  54602 | DBADMIN    | kurt     | vm002.zuhause | ACTIVE   |             23 | enq: TX - row lock contention |
```

In column SESSIONINFO blocked sessions are prefixed with ".." (maybe multiple times) to show some lock hierachy. The
line above is always the blocker for the session indented by "..".


### encrypt

Already discussed in chapter "Managing Passwords".


### df

List datafile infos.

Example list all datafiles sorted by "size" descending:
```bash
o df -o size_mb desc
    | FILE_TYPE   | TS         |   FILE_ID | FILE_NAME                                                        | STATUS   |   SIZE_MB |   USED_MB |   MAXSIZE_MB |   INCR_MB | AUTOEXTEND   | ONLINE_STATUS
----+-------------+------------+-----------+------------------------------------------------------------------+----------+-----------+-----------+--------------+-----------+--------------+-----------------
  0 | DATA        | UNDOTBS1   |        10 | /u02/oradata/CDB1/B6AEA844/datafile/o1_mf_undotbs1_hxqbxf0o_.dbf | AVAIL    |       435 |        23 |        32768 |         5 | YES          | ONLINE
  1 | DATA        | SYSAUX     |         9 | /u02/oradata/CDB1/B6AEA844/datafile/o1_mf_sysaux_hxqbxf0o_.dbf   | AVAIL    |       385 |       356 |        32768 |        10 | YES          | ONLINE
  2 | DATA        | SYSTEM     |         8 | /u02/oradata/CDB1/B6AEA844/datafile/o1_mf_system_hxqbxf0j_.dbf   | AVAIL    |       310 |       307 |        32768 |        10 | YES          | SYSTEM
  3 | DATA        | ADMIN_DATA |        12 | /u02/oradata/CDB1/B6AEA844/datafile/o1_mf_admin_da_hxwlwktt_.dbf | AVAIL    |       128 |        14 |         2048 |        64 | YES          | ONLINE
  4 | DATA        | RDF        |        13 | /u02/oradata/CDB1/B6AEA844/datafile/o1_mf_rdf_hy1tb1r3_.dbf      | AVAIL    |       128 |         3 |         4096 |         0 | YES          | ONLINE
  5 | TEMP        | TEMP       |         3 | /u02/oradata/CDB1/B6AEA844/datafile/o1_mf_temp_hxqbxf0p_.dbf     | UNDEF    |        47 |         0 |        32768 |         1 | YES          | N/A
  6 | DATA        | USERS      |        11 | /u02/oradata/CDB1/B6AEA844/datafile/o1_mf_users_hxqbxkmb_.dbf    | AVAIL    |         2 |         1 |        32768 |         1 | YES          | ONLINE
```

**Some remarks:**
As this command has a quite similar behaviour as command TS here, we also hav hints in place (gathered from a 19.9 database).
(Again objects inside the recyclebin and using view DBA_FREE_SPACE are the reason for these sometimes excessive runtimes.)


### find

This is about finding database objects by name or type ...

An example:
```bash
o find -f owner dbadmin -f name alert% --pdb all -u dbadmin
    | _db   | OWNER   | NAME      | TYPE         | STATUS   | CREATED    | LAST_DDL_TIME
----+-------+---------+-----------+--------------+----------+------------+-----------------
  0 | KB    | DBADMIN | ALERTLOG  | PACKAGE      | VALID    | 2021-07-10 | 2021-07-10
  1 | KB    | DBADMIN | ALERT_LOG | TABLE        | VALID    | 2021-07-10 | 2021-07-10
  2 | KB    | DBADMIN | ALERTLOG  | PACKAGE BODY | VALID    | 2021-07-10 | 2021-07-10
```

Here we are using 2 filter criterias:
* filter by owner (-f owner dbadmin)
* filter by name (-f name alert% ... a wildcard is used)


### genkey

Already discussed in chapter "Managing Passwords".


### list

Already discussed in chapter "List configuration details".


### par
Command PAR uses internally 2 different sources based on the SYSDBA flag for a given user. (Normally only SYS has SYSDBA privs.)
If you execute this a normal DBA, you only get public parameters. If you use e.g. SYS you also get hidden parameters!

#### E.g. "recovery related parameters":
* DBADMIN:
```bash
o par -f name %db%recov% --pdb kb -o name
    |   NUM | NAME                          | VALUE    | DEFAULT_VALUE   | ISDEFAULT   | SES_MODIFIABLE   | SYS_MODIFIABLE   | INST_MODIFIABLE   | MODIFIED   | ADJUSTED   | DEPRECATED   | BASIC   | UPDATE_COMMENT   | HIDDEN
----+-------+-------------------------------+----------+-----------------+-------------+------------------+------------------+-------------------+------------+------------+--------------+---------+------------------+----------
  0 |  2083 | db_recovery_file_dest         | /u02/fra | NONE            | FALSE       | FALSE            | IMMEDIATE        | FALSE             | FALSE      | FALSE      | FALSE        | TRUE    |                  | N
  1 |  2084 | db_recovery_file_dest_size    | 8G       | 0               | FALSE       | FALSE            | IMMEDIATE        | FALSE             | FALSE      | FALSE      | FALSE        | TRUE    |                  | N
  2 |  2186 | db_unrecoverable_scn_tracking | TRUE     | TRUE            | TRUE        | TRUE             | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                  | N
```

* SYS:
```bash
o par -f name %db%recov% --pdb kb -o name -u sys
    |   NUM | NAME                                    | VALUE    | DEFAULT_VALUE   | ISDEFAULT   | SES_MODIFIABLE   | SYS_MODIFIABLE   | INST_MODIFIABLE   | MODIFIED   | ADJUSTED   | DEPRECATED   | BASIC   | UPDATE_COMMENT   | HIDDEN
----+-------+-----------------------------------------+----------+-----------------+-------------+------------------+------------------+-------------------+------------+------------+--------------+---------+------------------+----------
  0 |  2328 | _clone_one_pdb_recovery                 | FALSE    | FALSE           | TRUE        | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
  1 |  1759 | _db_block_corruption_recovery_threshold | 5        | 5               | TRUE        | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
  2 |  2085 | _db_recovery_temporal_file_dest         |          | NONE            | TRUE        | FALSE            | IMMEDIATE        | FALSE             | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
  3 |  2231 | _skip_pdb_recovery_if_keystore_not_open | FALSE    | FALSE           | TRUE        | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
  4 |  2083 | db_recovery_file_dest                   | /u02/fra | NONE            | FALSE       | FALSE            | IMMEDIATE        | FALSE             | FALSE      | FALSE      | FALSE        | TRUE    |                  | N
  5 |  2084 | db_recovery_file_dest_size              | 8G       | 0               | FALSE       | FALSE            | IMMEDIATE        | FALSE             | FALSE      | FALSE      | FALSE        | TRUE    |                  | N
  6 |  2186 | db_unrecoverable_scn_tracking           | TRUE     | TRUE            | TRUE        | TRUE             | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                  | N
```
... We get additional matching hidden paramters here!

#### Another example (as SYS): Show all hidden parameters with non-default values
```bash
o par -f isdefault false -f hidden y --pdb kb -u sys -o name
    |   NUM | NAME                       | VALUE           |   DEFAULT_VALUE | ISDEFAULT   | SES_MODIFIABLE   | SYS_MODIFIABLE   | INST_MODIFIABLE   | MODIFIED   | ADJUSTED   | DEPRECATED   | BASIC   | UPDATE_COMMENT                   | HIDDEN
----+-------+----------------------------+-----------------+-----------------+-------------+------------------+------------------+-------------------+------------+------------+--------------+---------+----------------------------------+----------
  0 |  2525 | __data_transfer_cache_size | 0               |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
  1 |  1633 | __db_cache_size            | 14048M          |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
  2 |  2801 | __inmemory_ext_roarea      | 0               |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
  3 |  2799 | __inmemory_ext_rwarea      | 0               |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
  4 |   280 | __java_pool_size           | 128M            |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
  5 |   278 | __large_pool_size          | 32M             |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
  6 |   120 | __oracle_base              | /u01/app/oracle |                 | FALSE       | FALSE            | FALSE            | FALSE             | FALSE      | FALSE      | FALSE        | FALSE   | ORACLE_BASE set from environment | Y
  7 |  3869 | __pga_aggregate_target     | 4G              |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
  8 |  1559 | __sga_target               | 16G             |               0 | FALSE       | FALSE            | FALSE            | FALSE             | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
  9 |  1644 | __shared_io_pool_size      | 128M            |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
 10 |   276 | __shared_pool_size         | 2016M           |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
 11 |   282 | __streams_pool_size        | 0               |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
 12 |   284 | __unified_pga_pool_size    | 0               |               0 | FALSE       | FALSE            | IMMEDIATE        | TRUE              | FALSE      | FALSE      | FALSE        | FALSE   |                                  | Y
```

As all parameters have 2 leading "__", there is no "true" change of an hidden parameter here.

#### Another example: show values for hidden parameter across all databases tagged as "TEST"
```bash
o par -f name _lm_share_lock_opt --pdb all -u sys -t test
    | _db      |   NUM | NAME               | VALUE   | DEFAULT_VALUE   | ISDEFAULT   | SES_MODIFIABLE   | SYS_MODIFIABLE   | INST_MODIFIABLE   | MODIFIED   | ADJUSTED   | DEPRECATED   | BASIC   | UPDATE_COMMENT   | HIDDEN
----+----------+-------+--------------------+---------+-----------------+-------------+------------------+------------------+-------------------+------------+------------+--------------+---------+------------------+----------
  0 | GRZTST01 |  1146 | _lm_share_lock_opt | TRUE    | TRUE            | TRUE        | FALSE            | FALSE            | FALSE             | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
  0 | GRZTST02 |  1146 | _lm_share_lock_opt | TRUE    | TRUE            | TRUE        | FALSE            | FALSE            | FALSE             | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
  0 | GRZTST03 |  1146 | _lm_share_lock_opt | FALSE   | TRUE            | FALSE       | FALSE            | FALSE            | FALSE             | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
  0 | GRZTST04 |  1146 | _lm_share_lock_opt | FALSE   | TRUE            | FALSE       | FALSE            | FALSE            | FALSE             | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
  0 | GRZTST05 |  1146 | _lm_share_lock_opt | FALSE   | TRUE            | FALSE       | FALSE            | FALSE            | FALSE             | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
  0 | GRZTST07 |  1146 | _lm_share_lock_opt | FALSE   | TRUE            | FALSE       | FALSE            | FALSE            | FALSE             | FALSE      | FALSE      | FALSE        | FALSE   |                  | Y
```

### query

Already discussed in chapter "Using custom queries".


### ts

List tablespace infos.

Example 1 (simple filtering by name):
```bash
o ts -f name sys%
    | NAME   | STATUS   |   FILES | CONTENTS   | EXT_MGMT   | ALLOC_TYPE   | SEG_MGMT   |   SIZE_MB |   USED_MB |   MAXSIZE_MB |   USED_PCT | BIGFILE   | LOGGING
----+--------+----------+---------+------------+------------+--------------+------------+-----------+-----------+--------------+------------+-----------+-----------
  0 | SYSAUX | ONLINE   |       1 | PERMANENT  | LOCAL      | SYSTEM       | AUTO       |       385 |       356 |        32768 |          1 | NO        | YES
  1 | SYSTEM | ONLINE   |       1 | PERMANENT  | LOCAL      | SYSTEM       | MANUAL     |       310 |       307 |        32768 |          1 | NO        | YES
```

Example 2 (custom filtering "-f2" by size_mb):
```bash
o ts -f2 "size_mb >300"
    | NAME     | STATUS   |   FILES | CONTENTS   | EXT_MGMT   | ALLOC_TYPE   | SEG_MGMT   |   SIZE_MB |   USED_MB |   MAXSIZE_MB |   USED_PCT | BIGFILE   | LOGGING
----+----------+----------+---------+------------+------------+--------------+------------+-----------+-----------+--------------+------------+-----------+-----------
  0 | SYSAUX   | ONLINE   |       1 | PERMANENT  | LOCAL      | SYSTEM       | AUTO       |       385 |       356 |        32768 |          1 | NO        | YES
  1 | SYSTEM   | ONLINE   |       1 | PERMANENT  | LOCAL      | SYSTEM       | MANUAL     |       310 |       307 |        32768 |          1 | NO        | YES
  2 | UNDOTBS1 | ONLINE   |       1 | UNDO       | LOCAL      | SYSTEM       | MANUAL     |       435 |        23 |        32768 |          0 | NO        | YES
```

**Some remarks:**
When gathering tablespace infos you may experience quite "excessive" runtimes. This has to do with objects inside the recyclebin (see DBA_RECYCLEBIN).
Per default the recyclebin is activated. Typically performance is good again after you cleaned up the recyclebin. To provide stable runtimes, "TS" is
using hints gathered from an 19.9 database with an empty recyclebin (experimental feature).
Currently "TS" does not disdinguish between different database versions. (Maybe some future feature ...)


### usr

List basic information about database users. E.g.:
```bash
o usr -f ts admin_data
    | NAME       | ACC_STAT   | PROFILE   | TS         | TEMPTS   | CREATED             | ORA   | PWD_VERSIONS
----+------------+------------+-----------+------------+----------+---------------------+-------+----------------
  0 | C##DBADMIN | OPEN       | DEFAULT   | ADMIN_DATA | TEMP     | 2021-01-18 16:42:07 | N     | 11G 12C
  1 | DBADMIN    | OPEN       | DEFAULT   | ADMIN_DATA | TEMP     | 2020-12-19 19:52:38 | N     | 11G 12C
  2 | JOBTEST    | OPEN       | DEFAULT   | ADMIN_DATA | TEMP     | 2021-02-19 14:55:18 | N     | 11G 12C
```


# Related Stuff


## Setting up PYENV in "shared mode"

A typical setup for PYENV is local in your own HOME directory. That makes sense to minimze possible
conflicts with other users. For DBAs when managing a bigger database landscape it is definitely an
option to use a shared setup. The idea is to install PYENV once and use it from all database servers.
E.g. in a RAC envirmonent you might want to this setup only once on a shared disk (NFS).


### Requirements

You need to install some additional packages:
```bash
sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel
```
These are necessary to build python.


### Doing the setup

This is quite easy, just define the variable PYENV_ROOT upfront. This defines the root directory for PYENV.
Typically this is $HOME/.pyenv but you can adjust this.

```bash
export PYENV_ROOT="u00/python.pyenv"
```

Afterwards just execute:
```bash
curl https://pyenv.run | bash
```


### A ".bash_profile" file when using PYENV

This is just an example, but currently used in our setups:
```bash
# This script shall be sourced inside "$HOME/.bash_profile"!
# With this script all DBA's share the same basic environment with a fully functional python-setup.

# PYENV Setup ...
export PYENV_PATHS=/u00/python/.pyenv/bin:/u00/python/.pyenv/plugins/pyenv-virtualenv/shims:/u00/python/.pyenv/shims
export PATH=$PYENV_PATHS:$NO_ORA_PATH

export PYENV_ROOT="/u00/python/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

export GOROOT=/usr/local/go

# $PATH shall remain stable (also inside TMUX!). So no self-referencing of $PATH!
# We create it from scratch using $NO_ORA_PATH.
# (Look inside file "/etc/profile" to see how variable $NO_ORA_PATH is defined.)
export MYPATHS=$PYENV_PATHS:/usr/local/git/bin:$GOROOT/bin:$HOME/go/bin
export PATH=$MYPATHS:$NO_ORA_PATH

export PYTHONPATH=/u00/git/oratk/core/cmdline/python

# Working with ORATk ...
# (E.g. if you separate environments for PROD and TEST, you may need to adjust the "aliases"-script here ...)
export DBA_PATH=/u00/dba
source $DBA_PATH/environment/db-aliases-testrac.sh

alias o='python3 -m o'
```


### Reference information
Further details about how to install python environments and how to work with PYENV can be found here:
* https://realpython.com/intro-to-pyenv/
* https://github.com/pyenv/pyenv

... and on various other places ... ;)


### Setting up a local (and current) python environment

You need git as a prerequisite. This is quite easy:
```bash
sudo yum install git
```

Afterwards we can setup "pyenv" as already described above. Here we use the default path. (.pyenv in $HOME)
```bash
curl https://pyenv.run | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   270  100   270    0     0    277      0 --:--:-- --:--:-- --:--:--   277
Cloning into '/home/kurt/.pyenv'...
remote: Enumerating objects: 846, done.
remote: Counting objects: 100% (846/846), done.
remote: Compressing objects: 100% (445/445), done.
remote: Total 846 (delta 471), reused 521 (delta 297), pack-reused 0
Receiving objects: 100% (846/846), 445.31 KiB | 7.95 MiB/s, done.
Resolving deltas: 100% (471/471), done.
Cloning into '/home/kurt/.pyenv/plugins/pyenv-doctor'...
remote: Enumerating objects: 11, done.
remote: Counting objects: 100% (11/11), done.
remote: Compressing objects: 100% (9/9), done.
remote: Total 11 (delta 1), reused 2 (delta 0), pack-reused 0
Unpacking objects: 100% (11/11), 38.70 KiB | 1.38 MiB/s, done.
Cloning into '/home/kurt/.pyenv/plugins/pyenv-installer'...
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 16 (delta 1), reused 7 (delta 0), pack-reused 0
Unpacking objects: 100% (16/16), 5.73 KiB | 1.91 MiB/s, done.
Cloning into '/home/kurt/.pyenv/plugins/pyenv-update'...
remote: Enumerating objects: 10, done.
remote: Counting objects: 100% (10/10), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 10 (delta 1), reused 5 (delta 0), pack-reused 0
Unpacking objects: 100% (10/10), 2.83 KiB | 1.41 MiB/s, done.
Cloning into '/home/kurt/.pyenv/plugins/pyenv-virtualenv'...
remote: Enumerating objects: 61, done.
remote: Counting objects: 100% (61/61), done.
remote: Compressing objects: 100% (55/55), done.
remote: Total 61 (delta 11), reused 23 (delta 0), pack-reused 0
Unpacking objects: 100% (61/61), 37.87 KiB | 1.89 MiB/s, done.
Cloning into '/home/kurt/.pyenv/plugins/pyenv-which-ext'...
remote: Enumerating objects: 10, done.
remote: Counting objects: 100% (10/10), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 10 (delta 1), reused 6 (delta 0), pack-reused 0
Unpacking objects: 100% (10/10), 2.92 KiB | 1.46 MiB/s, done.

WARNING: seems you still have not added 'pyenv' to the load path.


See the README for instructions on how to set up
your shell environment for Pyenv.

Load pyenv-virtualenv automatically by adding
the following to ~/.bashrc:

eval "$(pyenv virtualenv-init -)"
```

For a basic setup you need at least these entries in your ".bash_profile":
```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

After restarting the shell you can list available python versions:
```bash
pyenv install --list | grep " 3"
```

I am choosing python 3.9.8 here. Python is built from scratch, so you se a lot of output!
```bash
pyenv install -v 3.9.8
```

After about 2 minutes the output ends with this:
```bash
WARNING: Additional context:
user = False
home = None
root = '/'
prefix = None
Looking in links: /tmp/tmpb5rkeytl
Processing /tmp/tmpb5rkeytl/setuptools-58.1.0-py3-none-any.whl
Processing /tmp/tmpb5rkeytl/pip-21.2.4-py3-none-any.whl
Installing collected packages: setuptools, pip
  WARNING: Value for scheme.headers does not match. Please report this to <https://github.com/pypa/pip/issues/10151>
  distutils: /home/kurt/.pyenv/versions/3.9.8/include/python3.9/setuptools
  sysconfig: /tmp/python-build.20211113203247.40496/Python-3.9.8/Include/setuptools
  WARNING: Value for scheme.headers does not match. Please report this to <https://github.com/pypa/pip/issues/10151>
  distutils: /home/kurt/.pyenv/versions/3.9.8/include/python3.9/pip
  sysconfig: /tmp/python-build.20211113203247.40496/Python-3.9.8/Include/pip
  WARNING: The scripts pip3 and pip3.9 are installed in '/home/kurt/.pyenv/versions/3.9.8/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed pip-21.2.4 setuptools-58.1.0
Installed Python-3.9.8 to /home/kurt/.pyenv/versions/3.9.8

/tmp/python-build.20211113203247.40496 ~
```

Checking available python versions:
```bash
pyenv versions
* system (set by /home/kurt/.pyenv/version)
  3.9.8
```

Change the python version for the current user. The python installed at system level is not harmed!
```bash
pyenv global 3.9.8
[kurt@vm003 ~]$ pyenv versions
  system
* 3.9.8 (set by /home/kurt/.pyenv/version)
```

Check if we really use python 3.9.8 now:
```bash
python
Python 3.9.8 (main, Nov 13 2021, 20:33:25)
[GCC 8.4.1 20200928 (Red Hat 8.4.1-1.0.4)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Upgrade "pip" (not mandatory, but you get warnings otherwise):
```bash
python -m pip install --upgrade pip
Requirement already satisfied: pip in ./.pyenv/versions/3.9.8/lib/python3.9/site-packages (21.2.4)
Collecting pip
  Downloading pip-21.3.1-py3-none-any.whl (1.7 MB)
     |████████████████████████████████| 1.7 MB 2.5 MB/s
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 21.2.4
    Uninstalling pip-21.2.4:
      Successfully uninstalled pip-21.2.4
Successfully installed pip-21.3.1
```


### Install the necessary python packages:

#### Pandas
```bash
pip install pandas
Collecting pandas
  Downloading pandas-1.3.4-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (11.5 MB)
     |████████████████████████████████| 11.5 MB 2.5 MB/s
Collecting python-dateutil>=2.7.3
  Downloading python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
     |████████████████████████████████| 247 kB 35.6 MB/s
Collecting pytz>=2017.3
  Downloading pytz-2021.3-py2.py3-none-any.whl (503 kB)
     |████████████████████████████████| 503 kB 33.2 MB/s
Collecting numpy>=1.17.3
  Downloading numpy-1.21.4-cp39-cp39-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (15.7 MB)
     |████████████████████████████████| 15.7 MB 43.9 MB/s
Collecting six>=1.5
  Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: six, pytz, python-dateutil, numpy, pandas
Successfully installed numpy-1.21.4 pandas-1.3.4 python-dateutil-2.8.2 pytz-2021.3 six-1.16.0
```

#### cx_Oracle
You can install this package without Oracle software (client or server) already installed, but to use
this package you need an Oracle installation!

```bash
pip install cx_Oracle
Collecting cx_Oracle
  Downloading cx_Oracle-8.3.0-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (888 kB)
     |████████████████████████████████| 888 kB 2.8 MB/s
Installing collected packages: cx-Oracle
Successfully installed cx-Oracle-8.3.0
```

 #### cryptography
This package is needed for strong password encryption.
```bash
pip install cryptography
Collecting cryptography
  Downloading cryptography-35.0.0-cp36-abi3-manylinux_2_24_x86_64.whl (3.5 MB)
     |████████████████████████████████| 3.5 MB 2.6 MB/s
Collecting cffi>=1.12
  Downloading cffi-1.15.0-cp39-cp39-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (444 kB)
     |████████████████████████████████| 444 kB 39.1 MB/s
Collecting pycparser
  Downloading pycparser-2.21-py2.py3-none-any.whl (118 kB)
     |████████████████████████████████| 118 kB 27.3 MB/s
Installing collected packages: pycparser, cffi, cryptography
Successfully installed cffi-1.15.0 cryptography-35.0.0 pycparser-2.21
```

#### tabulate
```bash
pip install tabulate
Collecting tabulate
  Downloading tabulate-0.8.9-py3-none-any.whl (25 kB)
Installing collected packages: tabulate
Successfully installed tabulate-0.8.9
```

#### pyarrow
This package is needed when saving query results as parquet-files.
```bash
pip install pyarrow
Collecting pyarrow
  Downloading pyarrow-6.0.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (25.6 MB)
     |████████████████████████████████| 25.6 MB 51.6 MB/s
Requirement already satisfied: numpy>=1.16.6 in /home/kurt/.pyenv/versions/3.9.8/lib/python3.9/site-packages (from pyarrow) (1.21.4)
Installing collected packages: pyarrow
Successfully installed pyarrow-6.0.0
```

#### openpyxl
This package is used to create ".xlsx" files
```bash
pip install openpyxl
Collecting openpyxl
  Downloading openpyxl-3.0.9-py2.py3-none-any.whl (242 kB)
     |████████████████████████████████| 242 kB 1.9 MB/s
Collecting et-xmlfile
  Downloading et_xmlfile-1.1.0-py3-none-any.whl (4.7 kB)
Installing collected packages: et-xmlfile, openpyxl
Successfully installed et-xmlfile-1.1.0 openpyxl-3.0.9
```

#### requirements-core.txt
So these toplevel requirements exists. (Additional dependencies are managed by pip.) This file is maintained inside directory "o":
```text
cryptography>=35.0.0
cx_Oracle>=8.3.0
openpyxl>=3.0.9
pandas>=1.3.4
pyarrow>=6.0.0
tabulate>=0.8.9
```

#### The complete script
```bash
pip install pandas
pip install cx_Oracle
pip install cryptography
pip install tabulate
pip install pyarrow
pip install openpyxl
```

## Using "o" in Windows
As all used packages are also available in Windows, setting up and using "o" is quite straightforward.
But there are some issues to consider ...


### Setting common environment variables
Typically these are set globally (Control panel / edit system environment variables).
```cmd
set ORACLE_HOME=<Oracle SW-HOME>
set PYENV=c:\progs\pyenv\pyenv-win
set PYTHONPATH=C:\progs\oratk\cmdline

set PATH=%PATH%;c:\progs\pyenv\pyenv-win\bin;c:\progs\pyenv\pyenv-win\shims
```

An Oracle Client Installation is a prerequisite to setup cx_Oracle!


### Installing "pyenv" for Windows
Check out https://github.com/pyenv-win/pyenv-win for all the details!

#### Get and install pyenv-win

1. Get the software: https://github.com/pyenv-win/pyenv-win/archive/master.zip

2. Move the content into directory "C:\progs" and rename the toplevel directory to "pyenv".
   So you have a match regarding environemt variable `%PYENV%`.

#### Configure Powershell
If you execute "pyenv" inside an old DOS-shell it will work immediately.
```cmd
pyenv
pyenv 2.64.11
Usage: pyenv <command> [<args>]

Some useful pyenv commands are:
   commands     List all available pyenv commands
   duplicate    Creates a duplicate python environment
   local        Set or show the local application-specific Python version
   global       Set or show the global Python version
   shell        Set or show the shell-specific Python version
   install      Install a Python version using python-build
   uninstall    Uninstall a specific Python version
   update       Update the cached version DB
   rehash       Rehash pyenv shims (run this after installing executables)
   vname        Show the current Python version
   version      Show the current Python version and its origin
   version-name Show the current Python version
   versions     List all Python versions available to pyenv
   exec         Runs an executable by first preparing PATH so that the selected Python
   which        Display the full path to an executable
   whence       List all Python versions that contain the given executable

See `pyenv help <command>' for information on a specific command.
For full documentation, see: https://github.com/pyenv-win/pyenv-win#readme
```

In Powershell this is not garuanteed! You may get something like:
```powershell
pyenv
pyenv : File C:\progs\pyenv\pyenv-win\bin\pyenv.ps1 cannot be loaded. The file C:\progs\pyenv\pyenv-win\bin\pyenv.ps1
is not digitally signed. You cannot run this script on the current system. For more information about running scripts
and setting execution policy, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ pyenv
+ ~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

Mircosoft even provides a link in the error-message decribing the situation and how to fix it!

See: (https:/go.microsoft.com/fwlink/?LinkID=135170)


To change the mode regarding script execution for the current user:
```powershell
Set-ExecutionPolicy -ExecutionPolicy UnRestricted -Scope CurrentUser

Execution Policy Change
The execution policy helps protect you from scripts that you do not trust. Changing the execution policy might expose
you to the security risks described in the about_Execution_Policies help topic at
https:/go.microsoft.com/fwlink/?LinkID=135170. Do you want to change the execution policy?
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): y
```

Now you can execute `pyenv` in the commandline, but you still get this warning eacht time you execute it:
```powershell
pyenv

Security warning
Run only scripts that you trust. While scripts from the internet can be useful, this script can potentially harm your
computer. If you trust this script, use the Unblock-File cmdlet to allow the script to run without this warning
message. Do you want to run C:\progs\pyenv\pyenv-win\bin\pyenv.ps1?
[D] Do not run  [R] Run once  [S] Suspend  [?] Help (default is "D"): Y
```

To permanently get rid of this warning unblock the script:
```powershell
Unblock-File C:\progs\pyenv\pyenv-win\bin\pyenv.ps1
```

Afterwards pyenv works also in Powershell without any issues.


#### Install Python
To list e.g. all available versions related to Python 3.10 you can do
```powershell
pyenv install -l | Select-String "3.10"

3.10.0-win32
3.10.0
3.10.1-win32
3.10.1
3.10.2-win32
3.10.2
3.10.3-win32
3.10.3
3.10.4-win32
3.10.4
```
... or something similar ...

**As local Administrator:** to install Python 3.10.4 (64bit) type:
```powershell
pyenv install -v 3.10.4
```

For some non-silent installs a wizard may pop up. Just confirm any proposed configurations!

#### Switch to your newly installed Python
Just do:
```powershell
pyenv global 3.10.4

python
Python 3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
```

See https://realpython.com/intro-to-pyenv/ for additional information regarding `pyenv`.


### Setting ORACMD_KEY
In the DOS-commandline you do it with:
```cmd
set ORACMD_KEY='<your key>'
```

In Powershell this is done with:
```powershell
$env:ORACMD_KEY='<your key>'
```


### Aliases
There are some quirks regarding aliases in Windows. Typing `python -m o` all the time is annoying,
so you need some shortcut (aka alias) here!

In the classic DOS-commandline you can use:
```cmd
doskey o=python3 -m o $*
```

In powershell this doskey-command is not working. I found this useful:
```powershell
function o {python3 -m o $args}
```


### Doing custom SQL-statments when inside a DOS-shell (cmd.exe)
Inside the old DOS-shell "$" has no special meaning. You always need double quotes (") when providing
some custom SQL-statement:
```cmd
o query -s 'select group#, bytes/1024/1024 mb from v$log' -d kb
```
... does NOT work !!!

But:
```cmd
o query -s "select group#, bytes/1024/1024 mb from v$log" -d kb
```

In the end this is quite nice, because you do not have to think about when to use single or double
quotes as you have to do in Linux.


### Doing custom SQL-statements when inside Powershell
Inside Powershell "$" has a meaning. So we have the same situation as in Linux here!

So this is just failing:
```powershell
o query -s "select group#, bytes/1024/1024 mb from v$log" -d kb

*** error executing command for database 'KB'! ***
ORA-00942: table or view does not exist
```
This is because "v$log" is changed into "v" as there is no variable "$log".

But you have some options here!
Keep using single quotes and escape them if necessary:
```powershell
o query -s 'select group#, status, bytes/1024/1024 mb from v$log where status=''CURRENT''' -d kb
    | _db   |   GROUP# | STATUS   |   MB
----+-------+----------+----------+------
  0 | KB    |        2 | CURRENT  |  200
```

Use double quotes and escape "$":
```powershell
o query -s "select group#, status, bytes/1024/1024 mb from v`$log where status='CURRENT'" -d kb
    | _db   |   GROUP# | STATUS   |   MB
----+-------+----------+----------+------
  0 | KB    |        2 | CURRENT  |  200
```
Powershell uses a single backquote to escape special symbols!


### Percent (%) cannot be used as a wildcard operator
This is some weird(?) behaviour in DOS-shell and in Powershell. If you do something like:
```powershell
o query -s "select *from v`$logfile where type like 'ON%'" -d kb -VV
Only 1 database: PARALLEL PROCESSING downgraded to SERIAL.
Processing database KB ...
Predicates = None
with QQQ as (select *from v$logfile where type like 'ON') select * from QQQ where 1=1  order by 1
connect to KB with provided username (DBADMIN) & password.
Elapsed time is 0.127 seconds for 1 database(s).
 _db   | GROUP#   | STATUS   | TYPE   | MEMBER   | IS_RECOVERY_DEST_FILE   | CON_ID
-------+----------+----------+--------+----------+-------------------------+----------
```
Verbosity was increased to get more details. And here we see that "%" just gets discarded!
This is because "%" is used to identify variables.

A preliminary solution is to just double the % sign.
*So always use "%%" instead of "%"!* This works inside DOS-cmdline and inside Powershell.

An example (look for %% !!!):
```powershell
o query -s "select *from v`$logfile where type like 'ON%%'" -d kb -VV
Only 1 database: PARALLEL PROCESSING downgraded to SERIAL.
Processing database KB ...
Predicates = None
with QQQ as (select *from v$logfile where type like 'ON%') select * from QQQ where 1=1  order by 1
connect to KB with provided username (DBADMIN) & password.
Elapsed time is 0.131 seconds for 1 database(s).
    | _db   |   GROUP# | STATUS   | TYPE   | MEMBER                                            | IS_RECOVERY_DEST_FILE   |   CON_ID
----+-------+----------+----------+--------+---------------------------------------------------+-------------------------+----------
  0 | KB    |        1 |          | ONLINE | /u02/oradata/CDB1/onlinelog/o1_mf_1_hxq8xpf5_.log | NO                      |        0
  1 | KB    |        2 |          | ONLINE | /u02/oradata/CDB1/onlinelog/o1_mf_2_hxq8xpok_.log | NO                      |        0
  2 | KB    |        3 |          | ONLINE | /u02/oradata/CDB1/onlinelog/o1_mf_3_hxq8xpxz_.log | NO                      |        0
```
