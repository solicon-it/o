import pandas as pd

from . import _base_class

# Some columns are commented out, because there is still some work to do here!
# E.g. column ISPDB_MODIFIABLE --> We would need further information from the database
# (version, CDB/PDB) to decide, if we can use it ...


def sqlStmt():
    return """
select
  num
 ,name
-- ,type
-- ,value
 ,display_value          VALUE
 ,default_value
 ,isdefault              ISDEFAULT
 ,isses_modifiable       SES_MODIFIABLE
 ,issys_modifiable       SYS_MODIFIABLE
-- ,ispdb_modifiable
 ,isinstance_modifiable  INST_MODIFIABLE
 ,ismodified             MODIFIED
 ,isadjusted             ADJUSTED
 ,isdeprecated           DEPRECATED
 ,isbasic                BASIC
-- ,description
 ,update_comment         UPDATE_COMMENT
-- ,hash
-- ,con_id
 ,'N'                    HIDDEN
from
   v$parameter
where 1=1
  {}
order by {}
"""


def sqlStmt_sys():
    return """
with PAR as (
select
   x.indx+1                                              NUM
  ,ksppinm                                               NAME
--  ,ksppity                                             TYPE
--  ,ksppstvl
  ,ksppstdvl                                             VALUE
  ,ksppstdfl                                             DEFAULT_VALUE
  ,ksppstdf                                              ISDEFAULT
  ,decode(bitand(ksppiflg/256,1),1,'TRUE','FALSE')       SES_MODIFIABLE
  ,decode(bitand(ksppiflg/65536,3)
          ,1,'IMMEDIATE'
          ,2,'DEFERRED'
          ,3,'IMMEDIATE'
          ,'FALSE')                                      SYS_MODIFIABLE
  ,decode(bitand(ksppiflg,4)
          ,4,'FALSE'
          ,decode(bitand(ksppiflg/65536,3)
                  ,0, 'FALSE', 'TRUE'
                 )
         )                                               INST_MODIFIABLE
  ,decode(bitand(ksppstvf,7)
          ,1,'MODIFIED'
          ,4,'SYSTEM_MOD'
          ,'FALSE')                                             MODIFIED
  ,decode(bitand(ksppstvf,2),2,'TRUE','FALSE')                  ADJUSTED
  ,decode(bitand(ksppilrmflg/64, 1), 1, 'TRUE', 'FALSE')        DEPRECATED
  ,decode(bitand(ksppilrmflg/268435456, 1), 1, 'TRUE', 'FALSE') BASIC
--  ,ksppdesc                                                   DESCRIPTION
  ,ksppstcmnt                                                   UPDATE_COMMENT
--  ,ksppihash                                                  HASH
  ,decode(substr(ksppinm,1,1),'_', 'Y', 'N')                    HIDDEN
from
  x$ksppi x
 ,x$ksppcv y 
where (x.indx = y.indx) 
  and x.inst_id = USERENV('Instance')
)
select * from PAR
where 1=1
  {}
order by {}
"""


class par(_base_class.OraCommand):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.cols = ['NUM', 'NAME', 'VALUE', 'DEFAULT', 'ISDEFAULT', 'SES_MODIFIABLE', 'SYS_MODIFIABLE', 'INST_MODIFIABLE',
                     'MODIFIED', 'ADJUSTED', 'DEPRECATED', 'BASIC', 'UPDATE_COMMENT', 'HIDDEN']

    def execute(self):
        super().checkColNames(self.ctx.filterExpr)

        predicateString = super().predicateExpr(
            super().adjustCase_forColumnValues(self.ctx.filterExpr, ['NAME']))

        # When we have a user with SYSDBA privs, we can directly access internal memory structures
        # to provide also information about hidden parameters.
        if self.ctx.session.user.sysdba:
            SQL = sqlStmt_sys().format(predicateString, super().sortExpr(self.ctx.sortExpr))
        else:
            SQL = sqlStmt().format(predicateString, super().sortExpr(self.ctx.sortExpr))
        super().printSQL(SQL)

        self.ctx.session.openConnection()
        df = pd.read_sql(SQL, con=self.ctx.session.connection)

        return df
