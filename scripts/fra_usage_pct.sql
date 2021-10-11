with FRA_USAGE_PCT as (
select
  max(decode(file_type, 'ARCHIVED LOG', percent_space_used, 0))  archivelogs
 ,max(decode(file_type, 'BACKUP PIECE', percent_space_used, 0))  backups
 ,max(decode(file_type, 'IMAGE COPY', percent_space_used, 0))    image_copies
 ,max(decode(file_type, 'FLASHBACK LOG', percent_space_used, 0)) flashback_logs
 ,sum(decode(file_type, 'CONTROL FILE', percent_space_used, 0)
     +decode(file_type, 'REDO LOG', percent_space_used, 0)
     +decode(file_type, 'FOREIGN ARCHIVED LOG', percent_space_used, 0)
     +decode(file_type, 'AUXILIARY DATAFILE COPY', percent_space_used, 0)) other
 ,sum(percent_space_used) total
from
  v$flash_recovery_area_usage
),
FRA_SIZE as (
select V.display_value RECO_DEST_SIZE from v$parameter V where name = 'db_recovery_file_dest_size'
)
select FRA_SIZE.*, FRA_USAGE_PCT.*
from
FRA_SIZE cross join FRA_USAGE_PCT;
