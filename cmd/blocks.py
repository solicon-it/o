import pandas as pd

from . import _base_class


def sqlStmt():
    return """
with LOCKS as (
select
  S.inst_id
 ,S.sid
 ,S.serial#
 ,P.spid
 ,S.username
 ,nvl(S.osuser, 'N/A') osuser
 ,S.machine
 ,S.blocking_instance
 ,S.blocking_session
 ,S.event
 ,S.status
 ,S.last_call_et
 ,decode(O.name, null, null, U.name||'.'||O.name) waiting_for
from
  gv$session S
inner join
  gv$process P on S.inst_id = P.inst_id
              and S.paddr   = P.addr
left outer join
  sys.obj$ O on O.obj# = S.row_wait_obj#
left outer join
  sys.user$ U on U.user# = O.owner#
)
select
  inst_id
 ,sessioninfo
 ,spid
 ,username
 ,osuser
 ,machine
 ,status
 ,last_call_et
 ,event
 ,waiting_for
from
(
  select distinct
    inst_id
   ,lpad('..',(level-1)*2,' ')||sid||','||serial#||',@'||inst_id sessioninfo
   ,spid
   ,username
   ,osuser
   ,machine
   ,sys_connect_by_path(sid,'/')
   ,status
   ,last_call_et
   ,event
   ,blocking_instance
   ,blocking_session
   ,waiting_for
  from
  (
    select * from LOCKS where blocking_session is not null
    union
    select A.*
    from
      LOCKS A
    inner join
      LOCKS B on A.inst_id = B.blocking_instance
             and A.sid     = B.blocking_session
  ) BLOCKS
  start with blocking_session is null
  connect by prior inst_id =  blocking_instance
         and prior sid     =  blocking_session
  order by sys_connect_by_path(sid,'/')
)
where 1=1
  {}
"""


class blocks(_base_class.OraCommand):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.cols = ['INST_ID', 'SESSIONINFO', 'SPID', 'USERNAME', 'OSUSER',
                     'MACHINE', 'STATUS', 'LAST_CALL_ET', 'EVENT', 'WAITING_FOR']

    def execute(self):
        super().checkColNames(self.ctx.filterExpr)

        predicateString = super().predicateExpr(
            super().adjustCase_forColumnValues(self.ctx.filterExpr, ['OSUSER', 'MACHINE']))
        SQL = sqlStmt().format(predicateString, super().sortExpr(self.ctx.sortExpr))
        super().printSQL(SQL)

        self.ctx.session.openConnection()
        df = pd.read_sql(SQL, con=self.ctx.session.connection)

        return df
