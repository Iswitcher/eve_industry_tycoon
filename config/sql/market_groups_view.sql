--drop old view
drop view if EXISTS market_groups_view;

--re-create new one
create view market_groups_view AS
select market_group_id
	,parent_group_id
	,has_types
	,icon_id
	,name_en as name
	,desc_en as desc, *
from market_groups
where end_date > DATE('now');

commit;