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
* Save a resultset back into some (Oracle) database or into some file (CSV, XSLX, PARQUET).


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
KB = ora.database(host='vm002', service_name='kb.zuhause', type='PDB', port=1521, version='19.9.0', tags = ['DEV'])
CDB1 = ora.database(host='vm002', service_name='cdb1.zuhause', type='CDB', port=1521, version='19.9.0')
CDB1.pdbs = [KB]
```
Basically you are introducing 2 new variables (KB, CDB1) as Oracle database objects containing some properties
and we relate these 2 databases by adding KB to the pdb-list of CDB1.

Property 'name' can be used as an shortcut for service-name. It is just a name for your database variable.
When emitting data from multiple databases 'name' is also shown in column '_db'.

Properties 'host', 'service_name' and 'port' are necessary to identify a database. Type-information (CDP / PDB / CLASSIC)
is used for additional filtering at the commandline (e.g. --pdb automatically enforces to use only databases with type 'PDB').

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

**Currently "o" can only process sql-scripts that contain exactly 1 sql-statment.**

Files containing multiple sql-statements or PL/SQL-blocks are not supported yet.


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


## Some remarks about commands in general

TDB ...


## Currently implemented commands

### blocks

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

