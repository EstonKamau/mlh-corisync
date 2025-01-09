SELECT 
    id AS enrollment_id,
    enrollment_date,
    enrolled,
    duration,
    created_at,
    updated_at,
    event_id_id AS event_id,
    user_id_id AS user_id,
    attended,
    completed_date,
    join_time
FROM {{source("mlh_data_warehouse","event_enrolment")}}