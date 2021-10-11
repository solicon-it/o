"""
This is just a configuration-file which contains accessible databases as regular python source.
With this approach it is quite easy use database-objects via "eval(..)".

*** ATTENTION ***
There are some rule here:
 * Each database- and user-object must be defined in uppercase.
 * Each tag must be defined in uppercase.
"""

import o.common.oracle as ora

# If you define variables inside this file always use at least 1 "_" !!!
_v = '19.9.0'


# Adjust this variable, if you want to use a custom directory for your SQL-scripts!
# ("None" means: check sub-directory "scripts")
_SQL_SCRIPT_DIR = None

# Databases and Users MUST NOT have leading "_" !!!

KB = ora.database(name='KB',     host='vm002',
                  tns='kb',   type='PDB', version=_v)
CDB1 = ora.database(name='CDB1', host='vm002', service_name='cdb1.zuhause',
                    type='CDB', rac=None, port=1521, version=_v)
CDB1.pdbs = [KB]

KB_Q = ora.database(name='KB_Q', host='vm002', service_name='kb_q.zuhause', type='PDB', rac=None, port=1521, version=_v, tags = ['Q'])
CDB2 = ora.database(name='CDB2', host='vm002', service_name='cdb2.zuhause', type='CDB', rac=None, port=1521, version=_v)
CDB2.pdbs = [KB_Q]


KURT = ora.user(name = 'KURT', sysdba = False)
KURT.set_pwd('kurt', [KB])

DBADMIN = ora.user(name = 'DBADMIN', sysdba = False)
DBADMIN.set_pwd('fernet:gAAAAABg2LE-pKcmFhVoMFOytdBniOAjFBV2R3kTfcRWEXYaeGRUgxV9zt3qUMf6o6t4irY1s_DTIcoAYDQ8OwylCQdG4LxuVA==',
                [KB, KB_Q])

SYS = ora.user(name = 'SYS', sysdba = True)
SYS.set_pwd('xxx', [KB, KB_Q, CDB1, CDB2])

DEFAULT_USER = DBADMIN
