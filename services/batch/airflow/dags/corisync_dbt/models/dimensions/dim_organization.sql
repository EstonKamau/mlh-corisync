SELECT 
        id AS organization_id,
        name AS organization_name,
        description AS organization_description,
        country,
        featured,
        organization_code,
        category,
        is_active,
        total_staffs,
        created_at,
        updated_at
FROM {{source('mlh_uat','organizations')}}