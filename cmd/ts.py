import pandas as pd

from . import _base_class


# USED_PCT is calculated with the sum (MAXBYTES) of all associated datafiles in a
# way correct values are displayed for autoextended and fixed sized files.
def sqlStmt():

    outline = """/*+
      BEGIN_OUTLINE_DATA
      IGNORE_OPTIM_EMBEDDED_HINTS
      OPTIMIZER_FEATURES_ENABLE('19.1.0')
      DB_VERSION('19.1.0')
      FIRST_ROWS
      OUTLINE_LEAF(@"SEL$DA17747E")
      MERGE(@"SEL$0EE6DB63" >"SEL$5")
      MERGE(@"SEL$A731BD80" >"SEL$5")
      OUTLINE_LEAF(@"SEL$EDBAFBC6")
      MERGE(@"SEL$03235BA3" >"SEL$11")
      MERGE(@"SEL$15" >"SEL$11")
      MERGE(@"SEL$97CCBC9E" >"SEL$11")
      OUTLINE_LEAF(@"SET$2")
      OUTLINE_LEAF(@"SEL$8E13D68A")
      PUSH_PRED(@"SEL$5C160134" "A"@"SEL$1" 2)
      OUTLINE_LEAF(@"SEL$19")
      OUTLINE_LEAF(@"SEL$5EC70623")
      MERGE(@"SEL$21" >"SEL$20")
      OUTLINE_LEAF(@"SEL$00A1922E")
      MERGE(@"SEL$23" >"SEL$22")
      OUTLINE_LEAF(@"SEL$24")
      OUTLINE_LEAF(@"SEL$25")
      OUTLINE_LEAF(@"SET$3")
      OUTLINE_LEAF(@"SEL$343B7E94")
      PUSH_PRED(@"SEL$5C160134" "F"@"SEL$1" 3)
      OUTLINE_LEAF(@"SEL$5C160134")
      MERGE(@"SEL$335DD26A" >"SEL$1")
      OUTLINE_LEAF(@"SEL$2F275C46")
      MERGE(@"SEL$5BC85507" >"SEL$30")
      OUTLINE_LEAF(@"SEL$685020DD")
      MERGE(@"SEL$79D9B115" >"SEL$35")
      MERGE(@"SEL$874CA85A" >"SEL$35")
      OUTLINE_LEAF(@"SET$4")
      OUTLINE_LEAF(@"SEL$3ECED2D6")
      PUSH_PRED(@"SEL$F718CC2F" "A"@"SEL$26" 2)
      OUTLINE_LEAF(@"SEL$A9A3EBBA")
      MERGE(@"SEL$3D91B1C1" >"SEL$49")
      OUTLINE_LEAF(@"SEL$96D14815")
      MERGE(@"SEL$27E47649" >"SEL$41")
      OUTLINE_LEAF(@"SEL$F718CC2F")
      MERGE(@"SEL$A065B7E5" >"SEL$26")
      OUTLINE_LEAF(@"SET$1")
      OUTLINE_LEAF(@"SEL$53")
      OUTLINE(@"SEL$5")
      OUTLINE(@"SEL$0EE6DB63")
      MERGE(@"SEL$10" >"SEL$9")
      OUTLINE(@"SEL$A731BD80")
      MERGE(@"SEL$8A3193DA" >"SEL$6")
      OUTLINE(@"SEL$11")
      OUTLINE(@"SEL$03235BA3")
      MERGE(@"SEL$1CF66C63" >"SEL$12")
      OUTLINE(@"SEL$15")
      OUTLINE(@"SEL$97CCBC9E")
      MERGE(@"SEL$17" >"SEL$16")
      OUTLINE(@"SEL$4")
      OUTLINE(@"SEL$20")
      OUTLINE(@"SEL$21")
      OUTLINE(@"SEL$22")
      OUTLINE(@"SEL$23")
      OUTLINE(@"SEL$18")
      OUTLINE(@"SEL$1")
      OUTLINE(@"SEL$335DD26A")
      MERGE(@"SEL$3" >"SEL$2")
      OUTLINE(@"SEL$30")
      OUTLINE(@"SEL$5BC85507")
      MERGE(@"SEL$AD150BAD" >"SEL$31")
      OUTLINE(@"SEL$35")
      OUTLINE(@"SEL$79D9B115")
      MERGE(@"SEL$40" >"SEL$39")
      OUTLINE(@"SEL$874CA85A")
      MERGE(@"SEL$62725911" >"SEL$36")
      OUTLINE(@"SEL$29")
      OUTLINE(@"SEL$49")
      OUTLINE(@"SEL$3D91B1C1")
      MERGE(@"SEL$A0A2DB7D" >"SEL$50")
      OUTLINE(@"SEL$41")
      OUTLINE(@"SEL$27E47649")
      MERGE(@"SEL$1822E6ED" >"SEL$42")
      OUTLINE(@"SEL$26")
      OUTLINE(@"SEL$A065B7E5")
      MERGE(@"SEL$28" >"SEL$27")
      OUTLINE(@"SEL$9")
      OUTLINE(@"SEL$10")
      OUTLINE(@"SEL$6")
      OUTLINE(@"SEL$8A3193DA")
      MERGE(@"SEL$8" >"SEL$7")
      OUTLINE(@"SEL$12")
      OUTLINE(@"SEL$1CF66C63")
      MERGE(@"SEL$14" >"SEL$13")
      OUTLINE(@"SEL$16")
      OUTLINE(@"SEL$17")
      OUTLINE(@"SEL$2")
      OUTLINE(@"SEL$3")
      OUTLINE(@"SEL$31")
      OUTLINE(@"SEL$AD150BAD")
      MERGE(@"SEL$8C085B80" >"SEL$32")
      OUTLINE(@"SEL$39")
      OUTLINE(@"SEL$40")
      OUTLINE(@"SEL$36")
      OUTLINE(@"SEL$62725911")
      MERGE(@"SEL$38" >"SEL$37")
      OUTLINE(@"SEL$50")
      OUTLINE(@"SEL$A0A2DB7D")
      MERGE(@"SEL$52" >"SEL$51")
      OUTLINE(@"SEL$42")
      OUTLINE(@"SEL$1822E6ED")
      MERGE(@"SEL$44" >"SEL$43")
      OUTLINE(@"SEL$27")
      OUTLINE(@"SEL$28")
      OUTLINE(@"SEL$7")
      OUTLINE(@"SEL$8")
      OUTLINE(@"SEL$13")
      OUTLINE(@"SEL$14")
      OUTLINE(@"SEL$32")
      OUTLINE(@"SEL$8C085B80")
      MERGE(@"SEL$34" >"SEL$33")
      OUTLINE(@"SEL$37")
      OUTLINE(@"SEL$38")
      OUTLINE(@"SEL$51")
      OUTLINE(@"SEL$52")
      OUTLINE(@"SEL$43")
      OUTLINE(@"SEL$44")
      OUTLINE(@"SEL$33")
      OUTLINE(@"SEL$34")
      NO_ACCESS(@"SEL$53" "TS"@"SEL$53")
      FULL(@"SEL$F718CC2F" "X$KCFISTSA"@"SEL$28")
      INDEX(@"SEL$F718CC2F" "TS"@"SEL$27" "I_TS#")
      INDEX(@"SEL$F718CC2F" "SVC"@"SEL$27" ("IMSVCTS$"."TS#"))
      NO_ACCESS(@"SEL$F718CC2F" "T"@"SEL$26")
      NO_ACCESS(@"SEL$F718CC2F" "A"@"SEL$26")
      LEADING(@"SEL$F718CC2F" "X$KCFISTSA"@"SEL$28" "TS"@"SEL$27" "SVC"@"SEL$27" "T"@"SEL$26" "A"@"SEL$26")
      USE_NL(@"SEL$F718CC2F" "TS"@"SEL$27")
      USE_NL(@"SEL$F718CC2F" "SVC"@"SEL$27")
      USE_HASH(@"SEL$F718CC2F" "T"@"SEL$26")
      USE_NL(@"SEL$F718CC2F" "A"@"SEL$26")
      FULL(@"SEL$5C160134" "X$KCFISTSA"@"SEL$3")
      INDEX(@"SEL$5C160134" "TS"@"SEL$2" "I_TS#")
      INDEX(@"SEL$5C160134" "SVC"@"SEL$2" ("IMSVCTS$"."TS#"))
      NO_ACCESS(@"SEL$5C160134" "A"@"SEL$1")
      NO_ACCESS(@"SEL$5C160134" "F"@"SEL$1")
      LEADING(@"SEL$5C160134" "X$KCFISTSA"@"SEL$3" "TS"@"SEL$2" "SVC"@"SEL$2" "A"@"SEL$1" "F"@"SEL$1")
      USE_NL(@"SEL$5C160134" "TS"@"SEL$2")
      USE_NL(@"SEL$5C160134" "SVC"@"SEL$2")
      USE_NL(@"SEL$5C160134" "A"@"SEL$1")
      USE_NL(@"SEL$5C160134" "F"@"SEL$1")
      NO_ACCESS(@"SEL$8E13D68A" "DBA_DATA_FILES"@"SEL$4")
      NO_ACCESS(@"SEL$343B7E94" "DBA_FREE_SPACE"@"SEL$18")
      INDEX_RS_ASC(@"SEL$25" "TS"@"SEL$25" ("TS$"."NAME"))
      FULL(@"SEL$25" "F"@"SEL$25")
      INDEX(@"SEL$25" "FI"@"SEL$25" ("FILE$"."TS#" "FILE$"."RELFILE#"))
      LEADING(@"SEL$25" "TS"@"SEL$25" "F"@"SEL$25" "FI"@"SEL$25")
      USE_NL(@"SEL$25" "F"@"SEL$25")
      USE_NL(@"SEL$25" "FI"@"SEL$25")
      INDEX_RS_ASC(@"SEL$24" "TS"@"SEL$24" ("TS$"."NAME"))
      INDEX_RS_ASC(@"SEL$24" "U"@"SEL$24" "I_FILE#_BLOCK#")
      INDEX_RS_ASC(@"SEL$24" "RB"@"SEL$24" ("RECYCLEBIN$"."TS#"))
      BATCH_TABLE_ACCESS_BY_ROWID(@"SEL$24" "RB"@"SEL$24")
      INDEX(@"SEL$24" "FI"@"SEL$24" ("FILE$"."TS#" "FILE$"."RELFILE#"))
      LEADING(@"SEL$24" "TS"@"SEL$24" "U"@"SEL$24" "RB"@"SEL$24" "FI"@"SEL$24")
      USE_NL(@"SEL$24" "U"@"SEL$24")
      USE_NL(@"SEL$24" "RB"@"SEL$24")
      USE_NL(@"SEL$24" "FI"@"SEL$24")
      INDEX_RS_ASC(@"SEL$00A1922E" "TS"@"SEL$22" ("TS$"."NAME"))
      INDEX_RS_ASC(@"SEL$00A1922E" "RB"@"SEL$22" ("RECYCLEBIN$"."TS#"))
      BATCH_TABLE_ACCESS_BY_ROWID(@"SEL$00A1922E" "RB"@"SEL$22")
      FULL(@"SEL$00A1922E" "X$KTFBUE"@"SEL$23")
      INDEX(@"SEL$00A1922E" "FI"@"SEL$22" ("FILE$"."TS#" "FILE$"."RELFILE#"))
      LEADING(@"SEL$00A1922E" "TS"@"SEL$22" "RB"@"SEL$22" "X$KTFBUE"@"SEL$23" "FI"@"SEL$22")
      USE_NL(@"SEL$00A1922E" "RB"@"SEL$22")
      USE_NL(@"SEL$00A1922E" "X$KTFBUE"@"SEL$23")
      USE_NL(@"SEL$00A1922E" "FI"@"SEL$22")
      INDEX_RS_ASC(@"SEL$5EC70623" "TS"@"SEL$20" ("TS$"."NAME"))
      FULL(@"SEL$5EC70623" "X$KTFBFE"@"SEL$21")
      INDEX(@"SEL$5EC70623" "FI"@"SEL$20" ("FILE$"."TS#" "FILE$"."RELFILE#"))
      LEADING(@"SEL$5EC70623" "TS"@"SEL$20" "X$KTFBFE"@"SEL$21" "FI"@"SEL$20")
      USE_NL(@"SEL$5EC70623" "X$KTFBFE"@"SEL$21")
      USE_NL(@"SEL$5EC70623" "FI"@"SEL$20")
      INDEX_RS_ASC(@"SEL$19" "TS"@"SEL$19" ("TS$"."NAME"))
      INDEX(@"SEL$19" "F"@"SEL$19" "I_TS#")
      INDEX(@"SEL$19" "FI"@"SEL$19" ("FILE$"."TS#" "FILE$"."RELFILE#"))
      LEADING(@"SEL$19" "TS"@"SEL$19" "F"@"SEL$19" "FI"@"SEL$19")
      USE_NL(@"SEL$19" "F"@"SEL$19")
      USE_NL(@"SEL$19" "FI"@"SEL$19")
      INDEX_RS_ASC(@"SEL$EDBAFBC6" "TS"@"SEL$11" ("TS$"."NAME"))
      FULL(@"SEL$EDBAFBC6" "X$KCCFN"@"SEL$14")
      FULL(@"SEL$EDBAFBC6" "X$KTFBHC"@"SEL$15")
      INDEX_RS_ASC(@"SEL$EDBAFBC6" "F"@"SEL$11" ("FILE$"."FILE#"))
      FULL(@"SEL$EDBAFBC6" "X$KCCFE"@"SEL$17")
      LEADING(@"SEL$EDBAFBC6" "TS"@"SEL$11" "X$KCCFN"@"SEL$14" "X$KTFBHC"@"SEL$15" "F"@"SEL$11" "X$KCCFE"@"SEL$17")
      USE_NL(@"SEL$EDBAFBC6" "X$KCCFN"@"SEL$14")
      USE_NL(@"SEL$EDBAFBC6" "X$KTFBHC"@"SEL$15")
      USE_NL(@"SEL$EDBAFBC6" "F"@"SEL$11")
      USE_NL(@"SEL$EDBAFBC6" "X$KCCFE"@"SEL$17")
      INDEX_RS_ASC(@"SEL$DA17747E" "TS"@"SEL$5" ("TS$"."NAME"))
      FULL(@"SEL$DA17747E" "F"@"SEL$5")
      FULL(@"SEL$DA17747E" "X$KCCFN"@"SEL$8")
      FULL(@"SEL$DA17747E" "X$KCCFE"@"SEL$10")
      LEADING(@"SEL$DA17747E" "TS"@"SEL$5" "F"@"SEL$5" "X$KCCFN"@"SEL$8" "X$KCCFE"@"SEL$10")
      USE_NL(@"SEL$DA17747E" "F"@"SEL$5")
      USE_HASH(@"SEL$DA17747E" "X$KCCFN"@"SEL$8")
      USE_NL(@"SEL$DA17747E" "X$KCCFE"@"SEL$10")
      NO_ACCESS(@"SEL$3ECED2D6" "DBA_TEMP_FILES"@"SEL$29")
      FULL(@"SEL$96D14815" "TS"@"SEL$44")
      FULL(@"SEL$96D14815" "FC"@"SEL$44")
      LEADING(@"SEL$96D14815" "TS"@"SEL$44" "FC"@"SEL$44")
      USE_NL(@"SEL$96D14815" "FC"@"SEL$44")
      USE_HASH_AGGREGATION(@"SEL$96D14815")
      FULL(@"SEL$A9A3EBBA" "X"@"SEL$52")
      FULL(@"SEL$A9A3EBBA" "Y"@"SEL$52")
      LEADING(@"SEL$A9A3EBBA" "X"@"SEL$52" "Y"@"SEL$52")
      USE_HASH(@"SEL$A9A3EBBA" "Y"@"SEL$52")
      FULL(@"SEL$685020DD" "X$KCCTF"@"SEL$38")
      FULL(@"SEL$685020DD" "FN"@"SEL$37")
      FULL(@"SEL$685020DD" "FH"@"SEL$37")
      FULL(@"SEL$685020DD" "HC"@"SEL$37")
      FULL(@"SEL$685020DD" "KS"@"SEL$40")
      FULL(@"SEL$685020DD" "KV"@"SEL$40")
      FULL(@"SEL$685020DD" "QU"@"SEL$40")
      FULL(@"SEL$685020DD" "X$KJIDT"@"SEL$40")
      INDEX(@"SEL$685020DD" "TS"@"SEL$35" "I_TS#")
      LEADING(@"SEL$685020DD" "X$KCCTF"@"SEL$38" "FN"@"SEL$37" "FH"@"SEL$37" "HC"@"SEL$37" "KS"@"SEL$40" "KV"@"SEL$40" 
              "QU"@"SEL$40" "X$KJIDT"@"SEL$40" "TS"@"SEL$35")
      USE_NL(@"SEL$685020DD" "FN"@"SEL$37")
      USE_NL(@"SEL$685020DD" "FH"@"SEL$37")
      USE_NL(@"SEL$685020DD" "HC"@"SEL$37")
      USE_HASH(@"SEL$685020DD" "KS"@"SEL$40")
      USE_MERGE_CARTESIAN(@"SEL$685020DD" "KV"@"SEL$40")
      USE_MERGE_CARTESIAN(@"SEL$685020DD" "QU"@"SEL$40")
      USE_MERGE_CARTESIAN(@"SEL$685020DD" "X$KJIDT"@"SEL$40")
      USE_NL(@"SEL$685020DD" "TS"@"SEL$35")
      FULL(@"SEL$2F275C46" "X$KCCTF"@"SEL$34")
      FULL(@"SEL$2F275C46" "FN"@"SEL$33")
      FULL(@"SEL$2F275C46" "FH"@"SEL$33")
      FULL(@"SEL$2F275C46" "HC"@"SEL$33")
      INDEX(@"SEL$2F275C46" "TS"@"SEL$30" "I_TS#")
      LEADING(@"SEL$2F275C46" "X$KCCTF"@"SEL$34" "FN"@"SEL$33" "FH"@"SEL$33" "HC"@"SEL$33" "TS"@"SEL$30")
      USE_NL(@"SEL$2F275C46" "FN"@"SEL$33")
      USE_NL(@"SEL$2F275C46" "FH"@"SEL$33")
      USE_NL(@"SEL$2F275C46" "HC"@"SEL$33")
      USE_NL(@"SEL$2F275C46" "TS"@"SEL$30")
      END_OUTLINE_DATA
  */
"""
    return """
with TS as (
SELECT
  -- <SQL app="sqlplus-tk" src="tablespaces.sql"/>
  d.tablespace_name name
 ,d.status
 ,a.files
 ,d.contents
 ,decode(d.extent_management,'DICTIONARY','DICT',d.extent_management) ext_mgmt
 ,d.allocation_type                                                   alloc_type
 ,d.segment_space_management                                          seg_mgmt
 ,round(NVL(a.bytes / 1024 / 1024, 0),0)                              size_mb
 ,round((NVL(a.bytes,0) - NVL(f.bytes,0))/1024/1024, 0)               used_mb
 ,round(NVL(a.maxbytes / 1024 / 1024, 0),0)                           maxsize_mb
 ,round((NVL(a.bytes,0) - NVL(f.bytes, 0)) / a.maxbytes * 100, 0)     used_pct
 ,d.bigfile                                                           bigfile
 ,decode(d.logging,'LOGGING','YES','NOLOGGING','NO','?')              logging
FROM
  sys.dba_tablespaces d
 ,(select
    tablespace_name
   ,sum(bytes) bytes
   ,decode(sign(sum(maxbytes)-sum(bytes)), 1, sum(maxbytes), sum(bytes)) maxbytes
   ,count(*) files
  from
    dba_data_files group by tablespace_name
  ) a 
 ,(select tablespace_name, sum(bytes) bytes
   from
     dba_free_space group by tablespace_name
  ) f
WHERE d.tablespace_name = a.tablespace_name(+)
  AND d.tablespace_name = f.tablespace_name(+)
  AND NOT (d.extent_management like 'LOCAL'
  AND d.contents like 'TEMPORARY')
UNION ALL
SELECT
  d.tablespace_name name
 ,d.status
 ,a.files
 ,d.contents
 ,decode(d.extent_management,'DICTIONARY','DICT',d.extent_management) ext_mgmt
 ,d.allocation_type                                                   alloc_type
 ,d.segment_space_management                                          seg_mgmt
 ,round(NVL(a.bytes / 1024 / 1024, 0),0)                              size_mb
 ,round((NVL(t.bytes,0))/1024/1024, 0)                                used_mb
 ,round(NVL(a.maxbytes / 1024 / 1024, 0),0)                           maxsize_mb
 ,round((NVL(t.bytes, 0)) / a.maxbytes * 100, 0)                      used_pct
 ,d.bigfile                                                           bigfile
 ,decode(d.logging,'LOGGING','YES','NOLOGGING','NO','?')              logging
FROM
  sys.dba_tablespaces d
 ,(select
    tablespace_name
   ,sum(bytes) bytes
   ,decode(sign(sum(maxbytes)-sum(bytes)), 1, sum(maxbytes), sum(bytes)) maxbytes
   ,count(*) files
  from
    dba_temp_files group by tablespace_name
  ) a 
 ,(select tablespace_name, sum(bytes_used) bytes
   from
     gv$temp_extent_pool group by tablespace_name
  ) t
WHERE d.tablespace_name = a.tablespace_name(+)
  AND d.tablespace_name = t.tablespace_name(+)
  AND d.extent_management like 'LOCAL'
  AND d.contents          like 'TEMPORARY'
)
select """ + outline + """
 * from TS
where 1=1
  {}
order by {}
"""


class ts(_base_class.OraCommand):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.cols = ['NAME', 'STATUS', 'FILES', 'CONTENT', 'EXT_MGMT', 'ALLOC_TYPE',
                     'SEG_MGMT', 'SIZE_MB', 'USED_MB', 'USED_PCT', 'BIGFILE', 'LOGGING']

    def execute(self):
        super().checkColNames(self.ctx.filterExpr)

        predicateString = super().predicateExpr(super().adjustCase_forColumnValues(self.ctx.filterExpr, []))
        SQL = sqlStmt().format(predicateString, super().sortExpr(self.ctx.sortExpr))

        self.ctx.session.openConnection()
        df = pd.read_sql(SQL, con=self.ctx.session.connection)

        return df

        
