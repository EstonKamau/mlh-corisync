SELECT 
    organization.organization_name,
    organization.organization_id,
    events.event_title,
    attendees.first_name,
    attendees.last_name,
    attendees.email,
    attendees.phone_number,
    initcap(COALESCE(attendees.gender,'Other')) gender,
    attendees.county,
    attendees.country,
    attendees.registration_number,
    attendees.profession,
    attendees.job_title,
    attendees.workplace,
    enrollment.duration,
    organization.category AS organization_category,
    enrollment.attended AS attended,
    enrollment.enrollment_date AS registration_time
FROM {{ref('dim_organization')}} organization
LEFT JOIN {{ref('fact_events')}} events ON organization.organization_id = events.organization_id
LEFT JOIN  {{ref('fact_enrollment')}} enrollment ON events.event_id = enrollment.event_id
LEFT JOIN {{ref('dim_attendees')}} attendees ON attendees.attendee_id = enrollment.user_id
WHERE events.event_title IS NOT NULL