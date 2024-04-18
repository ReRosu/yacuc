create table if not exists metrics_data(
	entity_id UInt32,
	dt DateTime64(3),
	metric_type UInt32,
	metric_value Float64
) ENGINE = MergeTree()
partition by metric_type
order by (entity_id, cityHash64(dt), metric_type)
sample by cityHash64(dt);

insert
	into
	metrics_data
SELECT
	*
FROM
	file(
'1_1974-04-26 12:52:22.975525_2024-04-13 12:52:22.975658_1_2024-04-13 12:52:23.124680.csv',
	'CSV',
	'entity_id UInt32, dt DateTime64(3), metric_type UInt32, metric_value Float64');