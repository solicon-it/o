#!/usr/bin/env python3

import logging
import argparse
import os
import os.path
import importlib
import o.common.oracle as ora
import o.common.manage_metadata as mm
import o.cmd.context as context

import time
from collections import namedtuple
from multiprocessing import Pool

import csv
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# VERSION INFORMATION:
# ====================
# 0.4.2 Bugfix: No error-message when we do not get results for some databases.
#       Flag -f2 with sql-scripts; Display SQL-stmt when using -VV
# 0.4.3 Oracle wallets as option when connecting to databases via "tnsnames.ora".
# 0.4.4 Bugfix: Saving results as files (HTML is new option)
#       DDL-Flag added

g_VERSION = '0.4.4'

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARN)

logging.info('Version: {}'.format(g_VERSION))

# "app.py" is in the project root directory. So we can use this directory as an offset.
# (e.g. useful when executing sql-scripts inside directory "scripts".)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_DIR = BASE_DIR + '/scripts'


def cmdline_args():
    # Process commandline-arguments, if present ...
    parser = argparse.ArgumentParser(description="""
A toolkit to work efficiently with Oracle databases direct in the Linux commandline. Currently
multiple basic commands (e.g. "usr") are implemented to support DBAs in their daily work.
""")
    parser.add_argument("command", nargs='?', default=None,
                        help="allowed are: 'blocks', 'encrypt', 'df', 'find', 'genkey', 'list', 'par', 'query', 'ts', 'usr', ...")

    parser.add_argument("-v", "--version", action="store_true",
                        help="show version information.")
    parser.add_argument("-V", "--verbose", action="count",
                        help="increase output verbosity")

    parser.add_argument("-D", "--ddl", dest="ddl", action="store_true",
                        help="To declare the current command or SQL-script as DDL-statement.")

    # We distinguish between "DB" (classic)", "CDB" and "PDB". This also works as an
    # implicit filter. (Class "database" has an attribute "type".)
    db_group = parser.add_mutually_exclusive_group(required=False)
    db_group.add_argument("-d", "--db", dest="db", action='append', nargs='+',
                          help="""A database name. Multiple names are possible -> the command is executed on all databases.
Use 'ALL', if you want to execute a command on all known databases.""")
    db_group.add_argument("--cdb", dest="cdb", action='append', nargs='+',
                          help="""A container database name.
Multiple names are possible -> the command is executed on all listed databases.
Use 'ALL', if you want to execute a command on all known container databases.""")
    db_group.add_argument("--pdb", dest="pdb", action='append', nargs='+',
                          help="""A pluggable database name.
Multiple names are possible -> the command is executed on all listed databases.
Use 'ALL', if you want to execute a command on all known pluggable databases.""")

    parser.add_argument("-t", "--tag", dest="tag", action='append', nargs='+',
                        help="One or multiple tags to provide additional filter criteria when selecting databases.")

    # User and password ...
    parser.add_argument("-u", "--usr", dest="usr", action='store',
                        help="The Oracle username which shall execute the given command.")
    parser.add_argument("-p", "--pwd", dest="pwd", action='store',
                        help="The Oracle username which shall execute the given command.")

    # custom queries ...
    query_group = parser.add_mutually_exclusive_group(required=False)
    query_group.add_argument("-s", "--sql", dest="sqlstmt", action='store',
                             help="A valid Oracle SQL statement.")
    query_group.add_argument("--file", dest="sqlfile", action='store',
                             help="A valid Oracle SQL statement in a separate file.")

    # Filtering and sorting ...
    parser.add_argument("-f", "--filter", dest="filter", action='append', nargs='+',
                        help="A filter condition: column-name (depends on the command you use) followed by some filter criteria.")
    parser.add_argument("-f2", "--filter2", dest="filter2", action='append', nargs='+',
                        help="A filter condition as string: 'column' operator <value>")
    parser.add_argument("-o", "--order", dest="order", action='append', nargs='+',
                        help="A column (see FILTER for possbile names) optionally followed by ASC or DESC.")

    # parallel processing ...
    process_group = parser.add_mutually_exclusive_group(required=False)
    process_group.add_argument("--parallel", dest="parallel", action='store', default=16,
                               help="Enable parallel processing (per default enabled with value = 16)")
    process_group.add_argument("--serial", dest="serial", action='store_true',
                               help="Force serial processing (per default disabled)")

    # Saving data ...
    parser.add_argument("--save", dest="save", action='append', nargs='+',
                        help="Saving results to CSV, HTML, XLSX, PARQUET or ORACLE")

    return parser.parse_args()


def filter_expr(simple_filter, filter_expr):
    filter = None
    if simple_filter and filter_expr:
        filter = simple_filter + filter_expr
    else:
        if simple_filter:
            filter = simple_filter
        else:
            filter = filter_expr

    return filter


def __check_sql(sql, starts_with):
    if sql.startswith(starts_with):
        print(
            f"This seems to be a DDL-statement ({starts_with.upper()} ...). Use flag --ddl / -D here!")
        exit(1)


def check_for_ddl_keywords(sqlstmt):
    sql = sqlstmt.strip().lower()
    __check_sql(sql, "create")
    __check_sql(sql, "alter")
    __check_sql(sql, "truncate")
    __check_sql(sql, "drop")
    __check_sql(sql, "grant")
    __check_sql(sql, "revoke")


par = namedtuple('par', 'cmd db usr')


def exec_command(par):
    # Used to execute some command on all/many Oracle databases at the same time.
    # "par" is a named-tuple (see definition above). The return value is a list
    # containing the database object and the results of the command. In case of an
    # error [db, <empty dataframe>] is the result!
    if par.cmd.ctx.verbose >= 1:
        print(f"Processing database {par.db.name} ...")

    par.cmd.ctx.session = ora.session(par.db, par.usr, par.cmd.ctx.verbose)

    try:
        df = par.cmd.execute()
        df.insert(loc=0, column='_db', value=par.db.name)
        return ['OK', par.db, df]
    except Exception as e:
        print(
            f"\n*** error executing command for database '{par.db.name}'! ***")
        print(f"User is '{par.usr.name}', error message is: {str(e)}\n")
        return ['ERR', par.db, pd.DataFrame()]


def run():
    # Check if we have ORACLE_HOME set ...
    if os.getenv('ORACLE_HOME') == None:
        print(
            "*** WARNING *** It seems we have no Oracle environment (ORACLE_HOME missing).")

    args = cmdline_args()

    if args.version:
        print("V " + g_VERSION + " - (c) solicon IT GmbH 2021")
        exit(0)

    if args.command not in ['blocks', 'df', 'encrypt', 'find', 'genkey', 'list', 'par', 'query', 'ts', 'usr']:
        print(f"[{args.command}] is not a valid command!")
        exit(1)

    # working with passwords ... ------------------------------------------------------------
    if args.command == "genkey":
        mm.generate_FernetKey()
        exit(0)

    if args.command == "encrypt":
        mm.encrypt_Password(args.pwd)
        exit(0)

    # additional checks / preparations ... --------------------------------------------------
    if args.command == "query" and args.sqlstmt and not args.ddl:
        # check if the SQL statement contains some DDL keywords ...
        check_for_ddl_keywords(args.sqlstmt)

    # Prepare the database list to be processed
    DBL = mm.database_list(args.db, args.cdb, args.pdb, args.tag)

    # listing config information ... --------------------------------------------------------
    if args.command == "list":
        if args.db or args.pdb or args.cdb:
            mm.print_db_list(DBL)
        elif args.sqlfile:
            mm.print_script_list(mm.script_dir(SCRIPT_DIR), args.sqlfile)
        exit(0)

    # normal commandline processing ... -----------------------------------------------------
    usr = mm.identify_user(args.usr, args.pwd)

    import pandas as pd
    from tabulate import tabulate

    filtering = filter_expr(args.filter, args.filter2)
    df_list = []

    cmdCtx = context.ctx(session=None,
                         filterExpr=filtering, sortExpr=args.order,
                         sqlStmt=args.sqlstmt,
                         sqlFile=args.sqlfile,
                         DDL=args.ddl,
                         scriptDir=mm.script_dir(SCRIPT_DIR),
                         verbose=args.verbose)

    # Dynamically import the necessary file to execute the given command
    cmd = importlib.import_module("o.cmd."+args.command)
    c = eval("cmd." + args.command + "(cmdCtx)")

    # do the proceessing parallel (default) or serial ...
    before = time.perf_counter()
    df_list = []
    if args.serial:
        if cmdCtx.verbose >= 1:
            print('SERIAL PROCESSING')
        for db in DBL:
            df = exec_command(par(c, db, usr))
            df_list.append(df)
    else:
        if len(DBL) > 1:
            if cmdCtx.verbose >= 1:
                print(
                    f'PARALLEL PROCESSING: maximum is {args.parallel} workers')
            params = list(
                map(lambda x: par(c, x, usr), DBL))

            # We start up to 16 (or whatever value was provided) parallel processes to
            # get data from Oracle databases.
            poolsize = int(args.parallel)
            if len(DBL) < poolsize:
                poolsize = len(DBL)
            with Pool(poolsize) as p:
                df_list = p.map(exec_command, params)
        else:
            if cmdCtx.verbose >= 1:
                print('Only 1 database: PARALLEL PROCESSING downgraded to SERIAL.')

            df = exec_command(par(c, DBL[0], usr))
            df_list.append(df)

    after = time.perf_counter()
    if cmdCtx.verbose >= 1:
        print("Elapsed time is {} seconds for {} database(s). ".format(
            str(round(after - before, 3)), len(DBL)))

    # processing results ... ---------------------------------------------------------------
    if df_list:
        df = []
        err = []
        for el in df_list:
            if el[0] == 'OK':
                df.append(el[2])
            else:
                err.append(el[1].name)

        if len(df) == 0:
            print(
                "\nThe command/query returned no results! (There will be no further output/file.)\n")
            exit(0)
        if args.save:
            df = pd.concat(df)
            fname = args.save[0][0]
            extension = os.path.splitext(fname)[1].lower()
            if extension not in ['.csv', '.xlsx', '.parquet', '.html']:
                print(f"'{extension}' is not a valid extension to save data!")
                exit(1)
            if extension == '.csv':
                df.to_csv(path_or_buf=fname, index=False,
                          quoting=csv.QUOTE_NONNUMERIC)
            elif extension == '.html':
                df.to_html(fname, index=False)
            elif extension == '.xlsx':
                df.to_excel(excel_writer=fname, index=False)
            elif extension == '.parquet':
                pa_table = pa.Table.from_pandas(df)
                pq.write_table(pa_table, fname)

            fsize = round(os.path.getsize(fname)/1024, 0)
            print(f"File '{fname}' created ({int(fsize)} kb).")

        else:
            # Print the final resultset (over all provided databases)
            print(tabulate(pd.concat(df), headers='keys', tablefmt='presto'))
            if err:
                print("\n*** ATTENTION ***")
                if len(err) == 1:
                    print(
                        "There was an error processing database '{}'!".format(err[0]))
                else:
                    print("There were errors processing databases '{}'!".format(err))
    else:
        print(
            "No database is a match for your [db/cdb/pdb - db-name - tag] pattern!")
