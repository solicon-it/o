select
  owner,count(*) cnt
from
  dba_objects
where status='INVALID'
group by owner
order by 1;
