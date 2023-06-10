with
REG as (
  select version_full v from dba_registry where comp_name='Oracle Database Catalog Views'
),
VERS as (
  select version_full v from v$instance
)
select REG.v version_database, VERS.v version_software
from REG cross join VERS
;
