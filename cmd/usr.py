import pandas as pd

from . import _base_class


def sqlStmt():
    return """
with USR as (
select
  username             name
 ,account_status       acc_stat
 ,profile
 ,default_tablespace   ts
 ,temporary_tablespace tempts
 ,to_char(created, 'yyyy-mm-dd hh24:mi:ss') created
 ,oracle_maintained    ora
 ,password_versions    pwd_versions
from
  dba_users
)
select * from USR
where 1=1
  {}
order by {}
"""


class usr(_base_class.OraCommand):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.cols = ['NAME', 'ACC_STAT', 'PROFILE', 'TS',
                     'TEMPTS', 'CREATED', 'ORA', 'PWD_VERSIONS']

    def execute(self):
        super().checkColNames(self.ctx.filterExpr)

        predicateString = super().predicateExpr(
            super().adjustCase_forColumnValues(self.ctx.filterExpr, []))
        SQL = sqlStmt().format(predicateString, super().sortExpr(self.ctx.sortExpr))
        super().printSQL(SQL)

        self.ctx.session.openConnection()
        df = pd.read_sql(SQL, con=self.ctx.session.connection)

        return df

        
