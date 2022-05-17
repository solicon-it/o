from typing import List, Tuple

import os
import re
import pandas as pd
from tabulate import tabulate
import o.common.oracle as ora
import o.cfg.databases as dbs
from cryptography.fernet import Fernet

# This module contains all sorts of (helper) stuff related to handle databases, users,
# passwords, ...


def script_dir(dir) -> str:
    if dbs._SQL_SCRIPT_DIR:
        return dbs._SQL_SCRIPT_DIR
    else:
        return dir


def osuser() -> str:
    userhome = os.path.expanduser('~')
    return os.path.split(userhome)[-1]


def user(name: str, handleUnknownUser: bool = False) -> ora.user or None:
    try:
        usr = eval("dbs."+name.upper())
        if isinstance(usr, ora.user):
            return usr
        else:
            Exception("no user")
    except:
        if handleUnknownUser:
            return None
        else:
            print("Can't identify '{}' as user - processing stopped!".format(name))
            exit(1)


def database(name: str) -> ora.database or None:
    try:
        db = eval("dbs."+name)
        if isinstance(db, ora.database):
            return db
        else:
            return None
    except:
        print("Can't identify '{}' as database - processing stopped!".format(name))
        exit(1)


def all_databases() -> List[ora.database]:
    return list(filter(lambda x: not x.startswith('_') and x != 'ora', dir(dbs)))


def DatabaseName_fromEnv() -> str or None:
    # In a typical Oracle environment we are using additional variables to control
    # the behaviour of our scripts. 'DBA_DB_NAME' contains database names in the
    # format 'CDB'_'PDB' or just a simple name, if it is a classic database setup.
    # This functions returns the database name from the current environment.
    try:
        db = os.environ['DBA_DB_NAME'].split('_')[-1]
    except:
        db = None
    return db


def database_list(dbs, cdbs, pdbs, tags):
    # Get a sorted list of database objects (see "databases.py") based on the provided
    # database names. ("cdbs" and "pdbs" imply a filter an database types.) In addtion
    # to that filtering can happen by database name ('ALL' keyword) and user defined
    # tags.

    dblist = list(filter(lambda x: x != None, [dbs, cdbs, pdbs]))
    if dblist:
        dblist = dblist[0]

    # Create the list of database names used as targets for the current command ...
    ALL_DBS = False
    if not dblist:
        DBL = DatabaseName_fromEnv()
        if DBL is None:
            DBL = []
        else:
            DBL = [DBL]
    else:
        DBL = list(set([item for sublist in dblist for item in sublist]))
        if DBL[-1].upper() == "ALL":
            DBL = all_databases()
            ALL_DBS = True

    # Create database objects from the list of database names. At this step we will
    # see, if some database is not defined ...
    DBL = [database(n) for n in [x.upper() for x in DBL]]
    DBL = [db for db in DBL if db]

    # Filter databases with RAC = SINGLE-NODE when using "all" databases ...
    if ALL_DBS:
        DBL = list(filter(lambda db: db.rac ==
                   'CLUSTER-SERVICE' or db.rac == None,  DBL))

    # Filter databases if we want to see only CDBs or PDBs ...
    dbtype = None
    if cdbs:
        dbtype = 'CDB'
    if pdbs:
        dbtype = 'PDB'
    if dbtype:
        DBL = list(filter(lambda db: db.type == dbtype,  DBL))

    # Filter by tags, if provided ...
    if tags:
        tagset = set([tag.upper() for tag in tags[0]])
        DBL = list(filter(lambda db: set(db.tags) & tagset, DBL))

    # Sort the final list of databases by name ...
    DBL.sort(key=lambda x: x.tns or x.service_name)

    return DBL


def print_db_list(DBL: List[ora.database]):
    # print the databases (with some config-details) according to the provided commandline
    # parameters.
    data = {'name':    list(map(lambda db: db.name, DBL)),
            'type':    list(map(lambda db: db.type, DBL)),
            'version': list(map(lambda db: db.version, DBL)),
            'tns':     list(map(lambda db: db.tns, DBL)),
            'service': list(map(lambda db: db.service_name, DBL)),
            'host':    list(map(lambda db: db.host, DBL)),
            'rac':     list(map(lambda db: db.rac, DBL)),
            'tags':    list(map(lambda db: db.tags, DBL))
            }
    df = pd.DataFrame(data)
    print(tabulate(df, headers='keys', tablefmt='presto'))


def print_script_list(scriptDir: str, fname: str):
    # print details about configured and existing files inside directory SCRIPT_DIR.

    do_regex = False
    if fname.lower() != 'all':
        p = re.compile(fname, re.IGNORECASE)
        do_regex = True

    # Pandas table with existing files ...
    FL = list(filter(lambda f: (f != 'scripts.csv'), os.listdir(scriptDir)))
    if do_regex:
        FL = list(filter(lambda f: p.match(f), FL))

    fdata = {'name': FL, 'status': list(map(lambda f: 'VALID', FL))}
    df_F = pd.DataFrame(fdata).set_index('name')

    # Pandas table with content of scripts.csv ...
    df = pd.read_csv(scriptDir+'/scripts.csv', index_col='name')
    if do_regex:
        L = list(filter(lambda f: p.match(f), df.index.tolist()))
        df = df.filter(items=L, axis=0)

    # Full outer join ...
    jDF = df.join(df_F, how='outer')
    # Necessary if only values from scripts.csv remain ...
    jDF['status'] = jDF['status'].apply(str)
    for f in jDF.index.tolist():
        if pd.isnull(jDF.at[f, 'type']):
            jDF.at[f, 'type'] = ''
            jDF.at[f, 'description'] = ''
            jDF.at[f, 'status'] = 'NO-CONFIG'
        if pd.isnull(jDF.at[f, 'status']):
            jDF.at[f, 'status'] = 'NO-FILE'

    # Print with reordered columns ...
    print(tabulate(jDF[["status", "type", "description"]
                       ].sort_index(), headers='keys', tablefmt='presto'))


def ORAtk_loginfile() -> str:
    # This file resides in directory $HOME/sqlplus-logins and can be identified by
    # using environment variables $DBA_DB_NAME and $USER. The name of these login
    # files always have the pattern <'$USER'-'$DBA_DB_NAME'.sql>.
    path = os.environ['HOME']+'/sqlplus-logins'
    try:
        file = os.environ['USER'] + '-' + os.environ['DBA_DB_NAME'] + '.sql'
    except:
        print("Environment variable $DBA_DB_NAME does not exist. Can't derive login information from directory $HOME/sqlplus-logins!")
        return None

    return path + '/' + file


def User_Pwd_fromEnv() -> Tuple[str, str, bool] or None:
    # Parse the loginfile (derived from the current environemnt). Return username
    # and password.
    loginfile = ORAtk_loginfile()
    if not loginfile:
        return None

    lines = list(open(loginfile, 'r'))
    connect = [x for x in lines if x.lstrip().startswith('conn')][0]
    words = re.split('[ /@]', ' '.join(connect.split()))

    usr = words[1]
    usr = None if usr == "" else usr
    pwd = words[2]
    pwd = None if pwd == "" else pwd

    sysdba = False
    if words[-1].lower() == 'sysdba':
        sysdba = True

    return (usr, pwd, sysdba)


def identify_user(username: str, pwd: str) -> ora.user:
    if username and pwd:
        # Option 1: user and password have been provided via commandline
        return ora.user(username, pwd)

    if username:
        return user(username)

    if not username and not pwd:
        # Check if the os-user is defined in "databases.py".
        usr = user(osuser(), handleUnknownUser=True)
        if usr:
            return usr

        # Fallback 1 (= Option 3): Check for dbs.DEFAULT_USER
        if dbs.DEFAULT_USER != None:
            return dbs.DEFAULT_USER
        else:
            # Fallback 2 (= Option 4): Use ORAtk environment
            user_tupel = User_Pwd_fromEnv()
            if user_tupel:
                (t_name, t_pwd, t_sysdba) = user_tupel
                usr = ora.user(t_name, t_pwd, t_sysdba)
                return usr
            else:
                # Last try: Get the username from the environment and see, if this user matches
                # with one of the users defined in "databases.py".
                print("Unable to identify an Oracle username - processing stopped!")
                exit(1)


def generate_FernetKey():
    key = Fernet.generate_key()
    print("Set environment variable ORACMD_KEY to use this key for encrypting passwords.")
    print("")
    print("KEY = {}".format(key.decode()))
    print("")
    print("... and keep it separatly in some password-manager, otherwise will NOT be able to decrypt your passwords in file 'databases.py'!")
    print("")


def fernet_key() -> str:
    try:
        return os.environ['ORACMD_KEY'].encode()
    except:
        print("Environment variable ORACMD_KEY is not set - processing stopped!")
        exit(1)


def encrypt_Password(pwd: str):
    if not pwd:
        print("No password provided! (use --pwd)")
        exit(1)

    key = fernet_key()

    fernet = Fernet(key)
    encPwd = fernet.encrypt(pwd.encode())

    print("Encrypted pwd = fernet:{}".format(encPwd.decode()))
