select group_concat(vv, ';') from (
select r, group_concat(v) vv from (
select rows.num r, cols.num c, ifnull(value, 0) v
from i rows
cross join i cols
left join c on rows.num = row_num and cols.num = col_num
order by rows.num, cols.num
) group by r order by r
);



select a.row_num as row_num, b.col_num as col_num, sum(a.value*b.value) as value
from a
join b on a.col_num = b.row_num
group by a.row_num, b.col_num
order by row_num, col_num;


