--drop old view
drop view if EXISTS market_items_view;

--re-create new one
create view market_items_view AS
select g.*
	,t.type_id
	,t.name_en as type_name
	,t.description_en
	,t.icon_id
	,t.market_group_id
	,t.volume
	,t.portion_size
	,t.base_price
from types t

left outer join (
	select c.*
		,g.group_id, g.name_en as group_name
	from group_ids g
	
	left outer join (
		select c.category_id, c.name_en as category_name
		from category_ids c
		where c.end_date > DATE('now')
		and c.is_published='true'
	) as c on g.category_id = c.category_id
	
	where end_date > DATE('now')
	and g.is_published = 'true'
) as g on t.group_id = g.group_id

where t.end_date > DATE('now')
and t.is_published='true'
and t.market_group_id is not NULL
order by g.category_id, g.group_id, t.type_id;

commit;

