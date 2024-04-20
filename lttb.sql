--Author github.com/ReRosu

CREATE OR REPLACE FUNCTION timestamp_diff(ft timestamp, st timestamp, r_t integer DEFAULT 0)
 RETURNS float8
 LANGUAGE plpgsql
AS $function$
declare 
 	f int;
 	e_f float8;
 	e_s float8;
begin
	case r_t then
		when 0 then -- diff in seconds
			f := 1;
		when 1 then -- diff in minutes
			f := 60;
		when 2 then -- diff in hours
			f := 60*60;
		when 3 then -- diff in days
			f := 60*60*24;
	end case;
	e_f := extract(epoch from ft);
	e_s := extract(epoch from st);
	return (e_f - e_s)/f;
END;
$function$
;


create TYPE if not exists ts_dot as (
    x timestamp,
    y float8
);

CREATE OR REPLACE FUNCTION lttb(left_b timestamp, right_b timestamp, e_id integer, metric_type integer, n_out integer)
 RETURNS TABLE(x timestamp, y float8)
 LANGUAGE plpgsql
AS $function$
declare
	not_sampled ts_dot[];
	sampled ts_dot[];
	every_ float8;
	a int;
	next_a int;
	start_tz timestamp;
	max_area_point ts_dot;
	avg_x float8;
	avg_y float8;
	avg_range_start int;
	avg_range_end int;
	avg_rang_end int; 
	avg_range_length int;
	range_offs int;
	range_to int;
	point_ax int;
	point_ay float8;
	max_area float8;
	area_ float8; 
begin
	not_sampled := array(select (dt, metric_value)::ts_dot from public.metrics_data where 
		(dt between left_b and right_b) and 
		entity_id = e_id
		order by dt asc);
	if array_length(not_sampled, 1) <= n_out then
		return query select * from unnest(not_sampled);
		return;
	end if;
	start_tz := not_sampled[1].x;
	every_ := (array_length(not_sampled, 1)::float8-2::float8)/(n_out::float8 - 2::float8);

	a := 1;
	next_a := 0;
	max_area_point := not_sampled[1];
	sampled := array_append(sampled, not_sampled[1]);

	for i in 1..n_out-2
	begin loop
		avg_x := 0;
		avg_y := 0;
		avg_range_start := (floor((i+0)*every_) + 1)::int;
		avg_range_end := (floor((i+1)*every_) + 1)::int;

		if avg_range_end < array_length(not_sampled, 1) then
			avg_rang_end := avg_range_end;
		else
			avg_rang_end := array_length(not_sampled, 1);
		end if;

		avg_range_length := avg_rang_end - avg_range_start;

--		avg_x := avg_range_length;
	
		for j in avg_range_start..avg_rang_end-1
		begin loop
			avg_x := avg_x + public.timestamp_diff(not_sampled[j].x, start_tz, 1);
			avg_y := avg_y + not_sampled[j].y;
		end loop;

		avg_range_start := avg_range_start + avg_range_length;

		avg_x := (avg_x / avg_range_length)::int;
        avg_y := (avg_y / avg_range_length)::int;
		
       	-- Get the range for this bucket
        range_offs := (floor((i + 0) * every_) + 1)::int;
        range_to := (floor((i + 1) * every_) + 1)::int;
        
        -- Point a
        point_ax := public.timestamp_diff(not_sampled[a].x, start_tz, 1);
        point_ay := not_sampled[a].y;
       
       	max_area := -1;
       
       	while range_offs < range_to loop
       		area_ := abs(
                (point_ax - avg_x)
                * (not_sampled[range_offs].y - point_ay)
                - (point_ax - range_offs) --not_sampled[range_offs][0])
                * (avg_y - point_ay)
            ) * 0.5;
           	if area_ > max_area then
                max_area := area_;
                max_area_point := not_sampled[range_offs];
                next_a := range_offs;  -- Next a is this b
            end if;
            range_offs := range_offs + 1;
       	end loop;
       	
       	sampled := array_append(sampled, max_area_point);
      	a := next_a;
       	
	end loop;
	
	sampled := array_append(sampled, not_sampled[array_length(not_sampled, 1)]);
	return query select * from unnest(sampled);
	return;

END;
$function$
;