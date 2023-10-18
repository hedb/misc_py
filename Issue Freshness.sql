

with 
raw_issues as (

    select 
        L.realm_id,
        date_trunc('week', activation_time) :: date as week_id,
        I.entity_id, I.severity_score, I.issue_id, 
        datediff('day', last_seen, date(activation_time)) as diff_in_days
    from issues as I inner join 
        (
            SELECT realm_id,unique_snapshot_id,activation_time from last_snapshots_v inner join snapshots_settings using (realm_id,snapshot_id)
        )  AS L using (unique_snapshot_id)
        inner join realm_parameters as rp on i.realm_id = rp.realm_id
    where 1=1
    -- and L.realm_id in ('bp')
    -- and L.realm_id in ('bp')
    and activation_time > dateadd(day,-31, current_date())
    and i.is_archived = FALSE
    and i.is_parent_archived = FALSE
    and i.scan_status in ('new','normal')
    and nvl(i.confidence, 100) >= nvl(rp.confidence, 0)
),

realm_percentiles as (
    select
        concat('Week: ',to_char(week_id , 'YYYY-MM-DD')) as week_id  ,realm_id,
      percentile_disc(0.50) within group (order by diff_in_days) as issue_age_p50_in_days,
      percentile_disc(0.60) within group (order by diff_in_days) as issue_age_p60_in_days,
      percentile_disc(0.70) within group (order by diff_in_days) as issue_age_p70_in_days,
      percentile_disc(0.80) within group (order by diff_in_days) as issue_age_p80_in_days,
      percentile_disc(0.90) within group (order by diff_in_days) as issue_age_p90_in_days,
      percentile_disc(0.95) within group (order by diff_in_days) as issue_age_p95_in_days

    from raw_issues

    group by 1,2
    order by week_id
        )
    , 
    issue_drilldown as (
    select
        realm_id,floor(diff_in_days / 10) * 10 as lower_limit,
        concat('\'',floor(diff_in_days / 10) * 10,'-',floor(diff_in_days / 10) * 10 + 10) 
            as diff_in_days, 
        severity_score, issue_id,
        count(1),
        ,min(entity_id) as sample1,        max(entity_id) as sample2,
    from raw_issues
    group by 1,2,3,4,5
    
)
    
-- select * from realm_percentiles
select * from issue_drilldown order by diff_in_days desc
;