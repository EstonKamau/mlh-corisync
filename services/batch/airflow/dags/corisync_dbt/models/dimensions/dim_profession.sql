SELECT 
    id event_cadre_id
    event_id,
    specialization_id
FROM {{source("mlh_uat","cadre")}}