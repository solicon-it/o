with
spid as (
select 
  P.spid, S.inst_id, S.sid, S.serial#
 ,S.username, S.osuser
 ,nvl(P.pname,S.program) program
 ,S.machine
 ,S.status
 ,S.event
 ,S.sql_id
 ,S.last_call_et
 ,round(P.cpu_used/1000000,0) cpu_used_secs
 ,round(pga_alloc_mem/1024/1024,0) pga_alloc_mb
 ,P.pname
from gv$session S
inner join
  gv$process P on S.inst_id = P.inst_id
              and S.paddr = P.addr
)
select * from spid;
