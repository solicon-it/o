import pandas as pd

from . import _base_class


def sqlStmt():
    return """
with OBJ as (
select
  O.owner
 ,O.object_name name
 ,O.object_type type
 ,O.status
 ,decode(trunc(O.created)
         ,trunc(sysdate), to_char(O.created,'hh24:mi')
         ,to_char(O.created,'yyyy-mm-dd')
  ) created
 ,decode(trunc(O.last_ddl_time)
         ,trunc(sysdate), to_char(O.last_ddl_time,'hh24:mi')
         ,to_char(O.last_ddl_time,'yyyy-mm-dd')
  ) last_ddl_time
from
  all_objects O
)
select * from  OBJ
where 1=1
  {}
order by {}
"""


class find(_base_class.OraCommand):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.cols = ['OWNER', 'NAME', 'TYPE',
                     'STATUS', 'CREATED', 'LAST_DDL_TIME']

    def execute(self):
        super().checkColNames(self.ctx.filterExpr)

        predicateString = super().predicateExpr(
            super().adjustCase_forColumnValues(self.ctx.filterExpr, []))
        SQL = sqlStmt().format(predicateString, super().sortExpr(self.ctx.sortExpr))
        super().printSQL(SQL)

        self.ctx.session.openConnection()
        df = pd.read_sql(SQL, con=self.ctx.session.connection)

        return df

