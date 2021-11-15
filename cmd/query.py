import os
import pandas as pd

from . import _base_class


def sqlfile(fname, scriptDir):
    qualified_filename = None
    p, f = os.path.split(fname)
    if p:
        qualified_filename = fname
    else:
        qualified_filename = scriptDir + '/' + fname

    if os.path.isfile(qualified_filename):
        f = open(qualified_filename)
        return f.read()
    else:
        print(
            f"sqlfile '{qualified_filename}' does not exist - processing stopped!")
        exit(1)


class query(_base_class.OraCommand):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.cols = []

    def execute(self):

        Q = None
        if self.ctx.sqlStmt:
            Q = self.ctx.sqlStmt
        else:
            Q = sqlfile(self.ctx.sqlFile, self.ctx.scriptDir)

        df = None

        # Assumption:
        # The query inside the file ends with a simple SELECT-clause (no WHERE predicates).
        # In this case we can easily add additional predicates defined per flag "-f2".
        SQL = Q.strip().rstrip(';')
        if self.ctx.DDL:
            if self.ctx.verbose >= 1:
                print("DDL-processing activated (no additional predicates no sorting).")
        else:
            SQL = SQL + " where 1=1 {} order by {}"
            predicateString = super().predicateExpr(
                super().adjustCase_forColumnValues(self.ctx.filterExpr, []))
            SQL = SQL.format(
                predicateString, super().sortExpr(self.ctx.sortExpr))

        super().printSQL(SQL)

        self.ctx.session.openConnection()
        if self.ctx.DDL:
            result = "OK"
            cur = self.ctx.session.connection.cursor()
            try:
                cur.execute(SQL)
            except Exception as e:
                result = str(e)

            df = pd.DataFrame({'DDL-Stmt': [SQL+';'], 'Result': [result]})
        else:
            df = pd.read_sql(SQL, con=self.ctx.session.connection)

        return df
