from typing import List

import os
import cx_Oracle as ora
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL

from cryptography.fernet import Fernet


def fernet_key() -> str:
    try:
        return os.environ['ORACMD_KEY'].encode()
    except:
        print("Environment variable ORACMD_KEY is not set - processing stopped!")
        exit(1)


class database:
    def __init__(self, name, tns=None, host=None, service_name=None, port=1521, version=None, type='CLASSIC', rac=None, tags=[]):

        # Name is a "shortcut" for service_name or some internal identifier. It is not
        # mandatory that the name here is related with the variable name of the db instance.
        self.name = name

        # With "tns" you can point to an existing entry in your "tnsnames.ora". This is
        # sometimes easier to configure, because "host", "service_name" and port can be omitted.
        # In more advanced setups (E.g. when combining RAC and container databases) you need
        # a tns-entry to connect to a specific instance on a spaecific node.
        # "tns" is used if you configure both variants.
        self.tns = tns

        # "host", "service_name" and "port" can be used, if you do not or do not want to use
        # a "tnsnames.ora" file.
        self.host = host
        self.service_name = service_name
        self.port = port

        # Currently the version is just for information only. In the future "version" may
        # influence some commands or the general behaviour.
        self.version = version

        self.type = type.upper()  # CDB, PDB or CLASSIC

        # None (single instance); CLUSTER-SERVICE, SINGLE-NODE
        # This classification is necessary to decide which database to include when operating
        # on lists (e.g. "all" keyword). If we have multiple instances of the same cluster in
        # our database list, we would get duplicate data, as we are using the same database
        # multiple times.
        if rac:
            self.rac = rac.upper()
        else:
            self.rac = None

        self.tags = tags

        # Only relevant for container databases. Currently parameter "pdbs" is not used.
        self.pdbs = []

    def dsn(self):
        if self.tns:
            return self.tns
        else:
            return ora.makedsn(self.host, (self.port or 1521), service_name=self.service_name)


class user:
    def __init__(self, name: str = None, pwd: str = None, sysdba: bool = False):
        self.name = name
        self.pwd = pwd
        self.sysdba = sysdba
        self.pwd_for_dbs = []
        self.wallet_for_dbs = []

        if self.name == 'SYS':
            self.sysdba = True

    def set_pwd(self, pwd: str, dbs: List[database]):
        self.pwd_for_dbs.append([pwd, dbs])

    def set_wallet(self, tns: str = None, db: database = None):
        self.wallet_for_dbs.append([tns, db])

    def decrypt_Password(self, encPwd: str) -> str:
        if not encPwd.startswith('fernet:'):
            # Password has been stored in plaintext!
            return encPwd

        key = fernet_key()

        fernet = Fernet(key)
        pwd = fernet.decrypt(encPwd[7:].encode())  # Honor prefix "fernet:" !!!
        return pwd.decode()

    def pwd_for_db(self, db: database) -> str:
        "return the plaintext password for the provided database."
        if self.pwd:
            return self.pwd
        else:
            for pw in self.pwd_for_dbs:
                if db in pw[1]:
                    return self.decrypt_Password(pw[0])
        return None

    def walletTNS_for_db(self, db: database) -> str:
        "return the tns-entry configured for access via wallet for the provided database."
        for tns in self.wallet_for_dbs:
            if db == tns[1]:
                return tns[0]
        return None


class session:
    def __init__(self, database: database, user: user, verbose: int = 0):
        self.database = database
        self.user = user
        self.verbose = verbose

    def openConnection(self):
        # Database connections are opened within commands. Exception handling happens inside the
        # main processing loop in 'app.py'.
        # Recent versions of pandas demand for "SqlAlchemy"! So this method uses SqlAlchemy to
        # create database connects and also provides SqlAlchemy connection objects.

        if self.user.name == None and self.user.sysdba == True:
            if self.verbose >= 2:
                print("{}: connect as sysdba (using os-group 'dba')".format(self.database.name))
            # connect as SYS with osuser-privs (dba) and ORACLE_SID setup ...
            self.connection = ora.connect("/", mode=ora.SYSDBA)
        else:
            pwd = self.user.pwd_for_db(self.database)
            wallet_tns = self.user.walletTNS_for_db(self.database)

            if not pwd and not wallet_tns:
                raise Exception(
                    "No password for {}@{} available!".format(self.user.name, self.database.service_name or self.database.tns))

            if pwd:
                if self.verbose >= 2:
                    print(
                        "connect to {} with provided username ({}) & password.".format(self.database.name, self.user.name))

                if self.user.sysdba:
                    self.connection = ora.connect(
                        self.user.name, pwd, dsn=self.database.dsn(), mode=ora.SYSDBA)
                else:
                    e = create_engine(
                                "oracle+cx_oracle://" + self.user.name + ":" + pwd + "@" +self.database.dsn())
                    self.connection = e.connect()

            if wallet_tns:
                usr = '/@' + wallet_tns
                if self.verbose >= 2:
                    print(
                        "using TNS-entry '{}' with wallet configuration (user '{}').".format(self.database.name, self.user.name))

                if self.user.sysdba:
                    if self.verbose >= 2:
                        print("connect as SYSDBA")
                    url = str(URL('oracle+cx_oracle', usr)) + '?mode=SYSDBA'
                    e = create_engine(url)
                    self.connection = e.connect()
                else:
                    if self.verbose >= 2:
                        print("connect normally")
                    e = create_engine(URL('oracle+cx_oracle', usr))
                    self.connection = e.connect()


    def openConnection_cx_ora(self):
        # Database connections are opened within commands. Exception handling happens inside the
        # main processing loop in 'app.py'.
        # This version uses the original cx_oracle way to create database sessions. The connection
        # objects are "cx_oracle" flavour.

        if self.user.name == None and self.user.sysdba == True:
            if self.verbose >= 2:
                print("{}: connect as sysdba".format(self.database.name))
            # connect as SYS with osuser-privs (dba) and ORACLE_SID setup ...
            self.connection = ora.connect("/", mode=ora.SYSDBA)
        else:
            pwd = self.user.pwd_for_db(self.database)
            wallet_tns = self.user.walletTNS_for_db(self.database)

            if not pwd and not wallet_tns:
                raise Exception(
                    "No password for {}@{} available!".format(self.user.name, self.database.service_name or self.database.tns))

            if pwd:
                if self.verbose >= 2:
                    print(
                        "connect to {} with provided username ({}) & password.".format(self.database.name, self.user.name))

                if self.user.sysdba:
                    self.connection = ora.connect(
                        self.user.name, pwd, dsn=self.database.dsn(), mode=ora.SYSDBA)
                else:
                    self.connection = ora.connect(
                        self.user.name, pwd, dsn=self.database.dsn())

            if wallet_tns:
                if self.verbose >= 2:
                    print(
                        "using TNS-entry '{}' with wallet configuration.".format(self.database.name))
                if self.user.sysdba:
                    self.connection = ora.connect(
                        dsn=wallet_tns, mode=ora.SYSDBA)
                else:
                    self.connection = ora.connect(dsn=wallet_tns)
