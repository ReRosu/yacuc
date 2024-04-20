create table if not exists metrics_data (
	entity_id int4 check(entity_id >= 0) not null,
	dt timestamp not null,
	metric_type int4 check(metric_type >= 0) not null,
	metric_value float8 not null
);
create index if not exists metrics_data_idx on metrics_data (entity_id, metric_type, dt);

DO
$do$
BEGIN
   IF (SELECT count(*) FROM metrics_data) = 0 THEN
      COPY metrics_data FROM '/user_files/1_1974-04-26 12:52:22.975525_2024-04-13 12:52:22.975658_1_2024-04-13 12:52:23.124680.csv' WITH (FORMAT csv, header true);
   END IF;
END
$do$;
