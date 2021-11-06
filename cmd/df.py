import pandas as pd

from . import _base_class


def sqlStmt():
    outline = """/*+
      BEGIN_OUTLINE_DATA
      INDEX(@"SEL$2F275C46" "TS"@"SEL$30" "I_TS#")
      USE_NL(@"SEL$2F275C46" "TS"@"SEL$30")
      INDEX(@"SEL$685020DD" "TS"@"SEL$35" "I_TS#")
      USE_NL(@"SEL$685020DD" "TS"@"SEL$35")
      INDEX(@"SEL$8C24855B" "TS"@"SEL$3" "I_TS#")
      USE_NL(@"SEL$8C24855B" "TS"@"SEL$3")
      FULL(@"SEL$FCA41E60" "TS"@"SEL$9")
      USE_HASH(@"SEL$FCA41E60" "TS"@"SEL$9")
      IGNORE_OPTIM_EMBEDDED_HINTS
      OPTIMIZER_FEATURES_ENABLE('19.1.0')
      DB_VERSION('19.1.0')
      FIRST_ROWS
      OUTLINE_LEAF(@"SEL$8C24855B")
      MERGE(@"SEL$8A3193DA" >"SEL$3")
      MERGE(@"SEL$F5B21678" >"SEL$3")
      OUTLINE_LEAF(@"SEL$FCA41E60")
      MERGE(@"SEL$13" >"SEL$9")
      MERGE(@"SEL$1FB6C052" >"SEL$9")
      MERGE(@"SEL$E3DF9B48" >"SEL$9")
      OUTLINE_LEAF(@"SET$1")
      OUTLINE_LEAF(@"SEL$20")
      OUTLINE_LEAF(@"SEL$109DB78D")
      MERGE(@"SEL$22" >"SEL$21")
      OUTLINE_LEAF(@"SEL$43F09110")
      MERGE(@"SEL$24" >"SEL$23")
      OUTLINE_LEAF(@"SEL$25")
      OUTLINE_LEAF(@"SEL$26")
      OUTLINE_LEAF(@"SET$2")
      OUTLINE_LEAF(@"SEL$66860544")
      PUSH_PRED(@"SEL$58ECF561" "FS"@"SEL$18" 1)
      OUTLINE_LEAF(@"SEL$58ECF561")
      MERGE(@"SEL$63D70E42" >"SEL$57")
      OUTLINE_LEAF(@"SEL$2F275C46")
      MERGE(@"SEL$5BC85507" >"SEL$30")
      OUTLINE_LEAF(@"SEL$685020DD")
      MERGE(@"SEL$79D9B115" >"SEL$35")
      MERGE(@"SEL$874CA85A" >"SEL$35")
      OUTLINE_LEAF(@"SET$3")
      OUTLINE_LEAF(@"SEL$65406569")
      MERGE(@"SEL$10CB9316" >"SEL$52")
      OUTLINE_LEAF(@"SEL$B85B7327")
      MERGE(@"SEL$6EE3C23C" >"SEL$44")
      OUTLINE_LEAF(@"SEL$11F7165E")
      MERGE(@"SEL$ADAE3EFF" >"SEL$58")
      OUTLINE_LEAF(@"SET$4")
      OUTLINE_LEAF(@"SEL$59")
      OUTLINE(@"SEL$3")
      OUTLINE(@"SEL$8A3193DA")
      MERGE(@"SEL$8" >"SEL$7")
      OUTLINE(@"SEL$F5B21678")
      MERGE(@"SEL$ABDE6DFF" >"SEL$4")
      OUTLINE(@"SEL$9")
      OUTLINE(@"SEL$13")
      OUTLINE(@"SEL$1FB6C052")
      MERGE(@"SEL$15" >"SEL$14")
      OUTLINE(@"SEL$E3DF9B48")
      MERGE(@"SEL$42DFC41A" >"SEL$10")
      OUTLINE(@"SEL$21")
      OUTLINE(@"SEL$22")
      OUTLINE(@"SEL$23")
      OUTLINE(@"SEL$24")
      OUTLINE(@"SEL$19")
      OUTLINE(@"SEL$57")
      OUTLINE(@"SEL$63D70E42")
      MERGE(@"SEL$6FD94BDB" >"SEL$1")
      OUTLINE(@"SEL$30")
      OUTLINE(@"SEL$5BC85507")
      MERGE(@"SEL$AD150BAD" >"SEL$31")
      OUTLINE(@"SEL$35")
      OUTLINE(@"SEL$79D9B115")
      MERGE(@"SEL$40" >"SEL$39")
      OUTLINE(@"SEL$874CA85A")
      MERGE(@"SEL$62725911" >"SEL$36")
      OUTLINE(@"SEL$52")
      OUTLINE(@"SEL$10CB9316")
      MERGE(@"SEL$43C3586C" >"SEL$53")
      OUTLINE(@"SEL$44")
      OUTLINE(@"SEL$6EE3C23C")
      MERGE(@"SEL$03AE7C5B" >"SEL$45")
      OUTLINE(@"SEL$58")
      OUTLINE(@"SEL$ADAE3EFF")
      MERGE(@"SEL$7EBC79E8" >"SEL$28")
      OUTLINE(@"SEL$7")
      OUTLINE(@"SEL$8")
      OUTLINE(@"SEL$4")
      OUTLINE(@"SEL$ABDE6DFF")
      MERGE(@"SEL$6" >"SEL$5")
      OUTLINE(@"SEL$14")
      OUTLINE(@"SEL$15")
      OUTLINE(@"SEL$10")
      OUTLINE(@"SEL$42DFC41A")
      MERGE(@"SEL$12" >"SEL$11")
      OUTLINE(@"SEL$1")
      OUTLINE(@"SEL$6FD94BDB")
      MERGE(@"SEL$963E9070" >"SEL$AA27515C")
      OUTLINE(@"SEL$31")
      OUTLINE(@"SEL$AD150BAD")
      MERGE(@"SEL$8C085B80" >"SEL$32")
      OUTLINE(@"SEL$39")
      OUTLINE(@"SEL$40")
      OUTLINE(@"SEL$36")
      OUTLINE(@"SEL$62725911")
      MERGE(@"SEL$38" >"SEL$37")
      OUTLINE(@"SEL$53")
      OUTLINE(@"SEL$43C3586C")
      MERGE(@"SEL$55" >"SEL$54")
      OUTLINE(@"SEL$45")
      OUTLINE(@"SEL$03AE7C5B")
      MERGE(@"SEL$47" >"SEL$46")
      OUTLINE(@"SEL$28")
      OUTLINE(@"SEL$7EBC79E8")
      MERGE(@"SEL$973BA8BC" >"SEL$7EF1AABD")
      OUTLINE(@"SEL$5")
      OUTLINE(@"SEL$6")
      OUTLINE(@"SEL$11")
      OUTLINE(@"SEL$12")
      OUTLINE(@"SEL$AA27515C")
      ANSI_REARCH(@"SEL$27")
      OUTLINE(@"SEL$963E9070")
      MERGE(@"SEL$5021FF29" >"SEL$A525FA86")
      OUTLINE(@"SEL$32")
      OUTLINE(@"SEL$8C085B80")
      MERGE(@"SEL$34" >"SEL$33")
      OUTLINE(@"SEL$37")
      OUTLINE(@"SEL$38")
      OUTLINE(@"SEL$54")
      OUTLINE(@"SEL$55")
      OUTLINE(@"SEL$46")
      OUTLINE(@"SEL$47")
      OUTLINE(@"SEL$7EF1AABD")
      ANSI_REARCH(@"SEL$56")
      OUTLINE(@"SEL$973BA8BC")
      MERGE(@"SEL$7EDA3D10" >"SEL$F2AB87B9")
      OUTLINE(@"SEL$27")
      OUTLINE(@"SEL$A525FA86")
      ANSI_REARCH(@"SEL$18")
      OUTLINE(@"SEL$5021FF29")
      MERGE(@"SEL$97CCBC9E" >"SEL$2")
      OUTLINE(@"SEL$33")
      OUTLINE(@"SEL$34")
      OUTLINE(@"SEL$56")
      OUTLINE(@"SEL$F2AB87B9")
      ANSI_REARCH(@"SEL$43")
      OUTLINE(@"SEL$7EDA3D10")
      MERGE(@"SEL$5BE7B2F8" >"SEL$29")
      OUTLINE(@"SEL$18")
      OUTLINE(@"SEL$2")
      OUTLINE(@"SEL$97CCBC9E")
      MERGE(@"SEL$17" >"SEL$16")
      OUTLINE(@"SEL$43")
      OUTLINE(@"SEL$29")
      OUTLINE(@"SEL$5BE7B2F8")
      MERGE(@"SEL$42" >"SEL$41")
      OUTLINE(@"SEL$16")
      OUTLINE(@"SEL$17")
      OUTLINE(@"SEL$41")
      OUTLINE(@"SEL$42")
      NO_ACCESS(@"SEL$59" "ALLFILES"@"SEL$59")
      NO_ACCESS(@"SEL$11F7165E" "DF"@"SEL$29")
      INDEX_RS_ASC(@"SEL$11F7165E" "TS"@"SEL$41" ("TS$"."NAME"))
      FULL(@"SEL$11F7165E" "X$KCFISTSA"@"SEL$42")
      INDEX(@"SEL$11F7165E" "SVC"@"SEL$41" ("IMSVCTS$"."TS#"))
      NO_ACCESS(@"SEL$11F7165E" "TP"@"SEL$43")
      LEADING(@"SEL$11F7165E" "DF"@"SEL$29" "TS"@"SEL$41" "X$KCFISTSA"@"SEL$42" "SVC"@"SEL$41" "TP"@"SEL$43")
      USE_NL(@"SEL$11F7165E" "TS"@"SEL$41")
      USE_NL(@"SEL$11F7165E" "X$KCFISTSA"@"SEL$42")
      USE_NL(@"SEL$11F7165E" "SVC"@"SEL$41")
      USE_HASH(@"SEL$11F7165E" "TP"@"SEL$43")
      NO_ACCESS(@"SEL$58ECF561" "DF"@"SEL$2")
      INDEX_RS_ASC(@"SEL$58ECF561" "TS"@"SEL$16" ("TS$"."NAME"))
      FULL(@"SEL$58ECF561" "X$KCFISTSA"@"SEL$17")
      INDEX(@"SEL$58ECF561" "SVC"@"SEL$16" ("IMSVCTS$"."TS#"))
      NO_ACCESS(@"SEL$58ECF561" "FS"@"SEL$18")
      LEADING(@"SEL$58ECF561" "DF"@"SEL$2" "TS"@"SEL$16" "X$KCFISTSA"@"SEL$17" "SVC"@"SEL$16" "FS"@"SEL$18")
      USE_NL(@"SEL$58ECF561" "TS"@"SEL$16")
      USE_NL(@"SEL$58ECF561" "X$KCFISTSA"@"SEL$17")
      USE_NL(@"SEL$58ECF561" "SVC"@"SEL$16")
      USE_NL(@"SEL$58ECF561" "FS"@"SEL$18")
      NO_ACCESS(@"SEL$66860544" "DBA_FREE_SPACE"@"SEL$19")
      INDEX_RS_ASC(@"SEL$26" "FI"@"SEL$26" ("FILE$"."FILE#"))
      FULL(@"SEL$26" "F"@"SEL$26")
      INDEX(@"SEL$26" "TS"@"SEL$26" "I_TS#")
      LEADING(@"SEL$26" "FI"@"SEL$26" "F"@"SEL$26" "TS"@"SEL$26")
      USE_NL(@"SEL$26" "F"@"SEL$26")
      USE_NL(@"SEL$26" "TS"@"SEL$26")
      INDEX_RS_ASC(@"SEL$25" "FI"@"SEL$25" ("FILE$"."FILE#"))
      INDEX_RS_ASC(@"SEL$25" "U"@"SEL$25" "I_FILE#_BLOCK#")
      INDEX_RS_ASC(@"SEL$25" "RB"@"SEL$25" ("RECYCLEBIN$"."TS#"))
      BATCH_TABLE_ACCESS_BY_ROWID(@"SEL$25" "RB"@"SEL$25")
      INDEX(@"SEL$25" "TS"@"SEL$25" "I_TS#")
      LEADING(@"SEL$25" "FI"@"SEL$25" "U"@"SEL$25" "RB"@"SEL$25" "TS"@"SEL$25")
      USE_NL(@"SEL$25" "U"@"SEL$25")
      USE_NL(@"SEL$25" "RB"@"SEL$25")
      USE_NL(@"SEL$25" "TS"@"SEL$25")
      INDEX_RS_ASC(@"SEL$43F09110" "FI"@"SEL$23" ("FILE$"."FILE#"))
      INDEX_RS_ASC(@"SEL$43F09110" "RB"@"SEL$23" ("RECYCLEBIN$"."TS#"))
      BATCH_TABLE_ACCESS_BY_ROWID(@"SEL$43F09110" "RB"@"SEL$23")
      INDEX(@"SEL$43F09110" "TS"@"SEL$23" "I_TS#")
      FULL(@"SEL$43F09110" "X$KTFBUE"@"SEL$24")
      LEADING(@"SEL$43F09110" "FI"@"SEL$23" "RB"@"SEL$23" "TS"@"SEL$23" "X$KTFBUE"@"SEL$24")
      USE_NL(@"SEL$43F09110" "RB"@"SEL$23")
      USE_NL(@"SEL$43F09110" "TS"@"SEL$23")
      USE_NL(@"SEL$43F09110" "X$KTFBUE"@"SEL$24")
      INDEX_RS_ASC(@"SEL$109DB78D" "FI"@"SEL$21" ("FILE$"."FILE#"))
      FULL(@"SEL$109DB78D" "X$KTFBFE"@"SEL$22")
      FULL(@"SEL$109DB78D" "TS"@"SEL$21")
      LEADING(@"SEL$109DB78D" "FI"@"SEL$21" "X$KTFBFE"@"SEL$22" "TS"@"SEL$21")
      USE_NL(@"SEL$109DB78D" "X$KTFBFE"@"SEL$22")
      USE_HASH(@"SEL$109DB78D" "TS"@"SEL$21")
      INDEX_RS_ASC(@"SEL$20" "FI"@"SEL$20" ("FILE$"."FILE#"))
      INDEX(@"SEL$20" "F"@"SEL$20" "I_TS#")
      INDEX(@"SEL$20" "TS"@"SEL$20" "I_TS#")
      LEADING(@"SEL$20" "FI"@"SEL$20" "F"@"SEL$20" "TS"@"SEL$20")
      USE_NL(@"SEL$20" "F"@"SEL$20")
      USE_NL(@"SEL$20" "TS"@"SEL$20")
      FULL(@"SEL$FCA41E60" "X$KCCFN"@"SEL$12")
      FULL(@"SEL$FCA41E60" "X$KTFBHC"@"SEL$13")
      FULL(@"SEL$FCA41E60" "F"@"SEL$9")
      FULL(@"SEL$FCA41E60" "X$KCCFE"@"SEL$15")
      LEADING(@"SEL$FCA41E60" "X$KCCFN"@"SEL$12" "X$KTFBHC"@"SEL$13" "TS"@"SEL$9" "F"@"SEL$9" "X$KCCFE"@"SEL$15")
      USE_NL(@"SEL$FCA41E60" "X$KTFBHC"@"SEL$13")
      USE_HASH(@"SEL$FCA41E60" "F"@"SEL$9")
      USE_NL(@"SEL$FCA41E60" "X$KCCFE"@"SEL$15")
      FULL(@"SEL$8C24855B" "F"@"SEL$3")
      FULL(@"SEL$8C24855B" "X$KCCFN"@"SEL$6")
      FULL(@"SEL$8C24855B" "X$KCCFE"@"SEL$8")
      LEADING(@"SEL$8C24855B" "F"@"SEL$3" "X$KCCFN"@"SEL$6" "X$KCCFE"@"SEL$8" "TS"@"SEL$3")
      USE_HASH(@"SEL$8C24855B" "X$KCCFN"@"SEL$6")
      USE_NL(@"SEL$8C24855B" "X$KCCFE"@"SEL$8")
      FULL(@"SEL$B85B7327" "TS"@"SEL$47")
      FULL(@"SEL$B85B7327" "FC"@"SEL$47")
      LEADING(@"SEL$B85B7327" "TS"@"SEL$47" "FC"@"SEL$47")
      USE_NL(@"SEL$B85B7327" "FC"@"SEL$47")
      USE_HASH_AGGREGATION(@"SEL$B85B7327")
      FULL(@"SEL$65406569" "X"@"SEL$55")
      FULL(@"SEL$65406569" "Y"@"SEL$55")
      LEADING(@"SEL$65406569" "X"@"SEL$55" "Y"@"SEL$55")
      USE_HASH(@"SEL$65406569" "Y"@"SEL$55")
      FULL(@"SEL$685020DD" "X$KCCTF"@"SEL$38")
      FULL(@"SEL$685020DD" "FN"@"SEL$37")
      FULL(@"SEL$685020DD" "FH"@"SEL$37")
      FULL(@"SEL$685020DD" "HC"@"SEL$37")
      FULL(@"SEL$685020DD" "KS"@"SEL$40")
      FULL(@"SEL$685020DD" "KV"@"SEL$40")
      FULL(@"SEL$685020DD" "QU"@"SEL$40")
      FULL(@"SEL$685020DD" "X$KJIDT"@"SEL$40")
      LEADING(@"SEL$685020DD" "X$KCCTF"@"SEL$38" "FN"@"SEL$37" "FH"@"SEL$37" "HC"@"SEL$37" "KS"@"SEL$40" "KV"@"SEL$40" 
              "QU"@"SEL$40" "X$KJIDT"@"SEL$40" "TS"@"SEL$35")
      USE_NL(@"SEL$685020DD" "FN"@"SEL$37")
      USE_NL(@"SEL$685020DD" "FH"@"SEL$37")
      USE_NL(@"SEL$685020DD" "HC"@"SEL$37")
      USE_HASH(@"SEL$685020DD" "KS"@"SEL$40")
      USE_MERGE_CARTESIAN(@"SEL$685020DD" "KV"@"SEL$40")
      USE_MERGE_CARTESIAN(@"SEL$685020DD" "QU"@"SEL$40")
      USE_MERGE_CARTESIAN(@"SEL$685020DD" "X$KJIDT"@"SEL$40")
      FULL(@"SEL$2F275C46" "X$KCCTF"@"SEL$34")
      FULL(@"SEL$2F275C46" "FN"@"SEL$33")
      FULL(@"SEL$2F275C46" "FH"@"SEL$33")
      FULL(@"SEL$2F275C46" "HC"@"SEL$33")
      LEADING(@"SEL$2F275C46" "X$KCCTF"@"SEL$34" "FN"@"SEL$33" "FH"@"SEL$33" "HC"@"SEL$33" "TS"@"SEL$30")
      USE_NL(@"SEL$2F275C46" "FN"@"SEL$33")
      USE_NL(@"SEL$2F275C46" "FH"@"SEL$33")
      USE_NL(@"SEL$2F275C46" "HC"@"SEL$33")
      END_OUTLINE_DATA
  */
"""
    return """
with
DATAFILE as (
  select
    file_type, tablespace_name, file_id, file_name, status
   ,filesize_mb
   ,filesize_used_mb
   ,decode(autoextensible, 'YES', filesize_max_mb, null) filesize_max_mb
   ,increment_by_mb, autoextensible, online_status
  from
  (
    select
      'DATA' file_type
     ,DF.tablespace_name
     ,DF.file_id
     ,DF.file_name
     ,decode(DF.status, 'INVALID', 'INVALID', 'AVAILABLE', 'AVAIL', 'UNDEF') status
     ,round(DF.bytes/1024/1024, 0) filesize_mb
     ,round((DF.bytes - nvl(FS.bytes,0))/1024/1024, 0) filesize_used_mb
     ,round(decode(DF.autoextensible, 'YES', DF.maxbytes, DF.bytes)/1024/1024, 0) filesize_max_mb
     ,decode(DF.autoextensible, 'YES', round(DF.increment_by*TS.block_size/1024/1024, 0), null) increment_by_mb
     ,DF.autoextensible
     ,DF.online_status
    from
      dba_data_files DF
    inner join
      dba_tablespaces TS on TS.tablespace_name = DF.tablespace_name
    left outer join
      (select file_id, sum(bytes) bytes from dba_free_space group by file_id) FS on DF.file_id = FS.file_id
  )
),
TEMPFILE as (
  select
    file_type, tablespace_name, file_id, file_name, status
   ,filesize_mb
   ,filesize_used_mb
   ,decode(autoextensible, 'YES', filesize_max_mb, null) filesize_max_mb
   ,increment_by_mb, autoextensible, online_status
  from
  (
  select
    'TEMP' file_type
   ,DF.tablespace_name
   ,DF.file_id
   ,DF.file_name
   ,decode(DF.status, 'INVALID', 'INVALID', 'AVAILABLE', 'AVAIL', 'UNDEF') status
   ,round(DF.bytes/1024/1024, 0) filesize_mb
   ,round(TP.bytes/1024/1024,0 ) filesize_used_mb
   ,round(decode(DF.autoextensible, 'YES', DF.maxbytes, DF.bytes)/1024/1024, 0) filesize_max_mb
   ,decode(DF.autoextensible, 'YES', round(DF.increment_by*TS.block_size/1024/1024, 0), null) increment_by_mb
   ,DF.autoextensible
   ,'N/A' online_status
  from
    dba_temp_files DF
  inner join
    dba_tablespaces TS on TS.tablespace_name = DF.tablespace_name
  left outer join 
    (select file_id, sum(bytes_used) bytes from gv$temp_extent_pool group by file_id) TP on TP.file_id = DF.file_id
  )
),
ALLFILES as (
select
  file_type
 ,tablespace_name ts
 ,file_id
 ,file_name
 ,status
 ,filesize_mb       size_mb
 ,filesize_used_mb  used_mb
 ,filesize_max_mb   maxsize_mb
 ,increment_by_mb   incr_mb
 ,autoextensible    autoextend
 ,online_status
from
  DATAFILE
union all
select
  file_type
 ,tablespace_name ts
 ,file_id
 ,file_name
 ,status
 ,filesize_mb       filesize_mb
 ,filesize_used_mb  used_mb
 ,filesize_max_mb   maxsize_mb
 ,increment_by_mb   incr_mb
 ,autoextensible    autoextend
 ,online_status
from
  TEMPFILE
)
select """ + outline + """ *
from
  ALLFILES
where 1=1
  {}
order by {}
"""


class df(_base_class.OraCommand):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.cols = ['FILE_TYPE', 'TS', 'FILE_ID', 'FILE_NAME', 'STATUS', 'SIZE_MB', 'USED_MB', 'MAXSIZE_MB',
                     'INCR_MB', 'AUTOEXTEND', 'ONLINE_STATUS']

    def execute(self):
        super().checkColNames(self.ctx.filterExpr)

        predicateString = super().predicateExpr(
            super().adjustCase_forColumnValues(self.ctx.filterExpr, ['FILE_NAME']))
        SQL = sqlStmt().format(predicateString, super().sortExpr(self.ctx.sortExpr))
        super().printSQL(SQL)

        self.ctx.session.openConnection()
        df = pd.read_sql(SQL, con=self.ctx.session.connection)

        return df

