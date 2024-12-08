import pandas as pd
import json
from google.cloud import storage
from datetime import timedelta, datetime
from io import StringIO
from airflow import DAG
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.python_operator import PythonOperator

# define default for DAGS
default_args = {
    'owner': 'tc4a',
    'start_date': datetime(2023, 11, 13),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# create dags instance
dag = DAG(
    'tc4a_data_visualization',
    default_args=default_args,
    description='An Airflow DAG for tc4a Postgres to BigQuery',
    schedule_interval='@daily',
    catchup=False
)

# Bigquery config parameters
BQ_CON_ID = "gcp_connection"
BQ_PROJECT = "visualization-app-404406"
BQ_DATASET = "tc4a"
BQ_TABLE1 = "bq_ngo"
BQ_TABLE2 = "bq_hospitals"
BQ_TABLE3 = "bq_pharmas"
BQ_TABLE4 = "bq_associations"
BQ_TABLE5 = "bq_avenue"
BQ_TABLE6 = "bq_ccare"
BQ_BUCKET = 'tc4a-backet'

# Postgres Config variables
PG_CON_ID = "postgres_default"
PG_SCHEMA = "public"

date_suffix = datetime.now().strftime("%Y%m%d")

def standardize_country_name(country_name):
    """
    Function to standardize country names.
    Ensures that the first letter of each word is capitalized.
    """
    if isinstance(country_name, str):
        return country_name.strip().title()
    return country_name

def sanitize_gender(gender):
    """
    Function to sanitize the gender field.
    Maps 'male' to 'Male', 'female' to 'Female',
    and handles null or empty values by assigning 'Other'.
    """
    if pd.isna(gender) or gender.strip() == '':
        return 'Other'
    gender = gender.strip().capitalize()
    if gender.lower() in ['male', 'female']:
        return gender.capitalize()
    return 'Other'

def sanitize_field_name(name):
    # Replace unsupported characters with underscores
    return name.replace(' ', '_').replace('/', '_').replace('-', '_').replace('?', '') \
        .replace('.', '').replace('(', '').replace(')', '').replace(',', '_').lower()

def merge_columns(df, new_col_name, columns_to_merge):
    existing_columns = [col for col in columns_to_merge if col in df.columns]
    if existing_columns:
        df[new_col_name] = df[existing_columns].bfill(axis=1).iloc[:, 0]
        df.drop(columns=[col for col in existing_columns if col != new_col_name], inplace=True)
    return df

# Define a function to transform the data
def transform_data(entity):
    client = storage.Client()
    bucket = client.bucket(BQ_BUCKET)

    raw_file = f'{entity}_raw_data_{date_suffix}.csv'
    transformed_file = f'/tmp/{entity}_transformed_data_{date_suffix}.csv'

    blob = bucket.blob(raw_file)
    content = blob.download_as_text()
    df = pd.read_csv(StringIO(content))

    def extract_json_to_columns(row):
        if isinstance(row, pd.Series) and 'other_info' in row:
            other_info = row['other_info']
            if isinstance(other_info, str):
                other_info = other_info.replace("'", '"')
                try:
                    other_info_dict = json.loads(other_info)
                    # Safely remove 'other_info'
                    row = row.drop('other_info')  
                    for key, value in other_info_dict.items():
                        sanitized_key = sanitize_field_name(key)
                        row[sanitized_key] = value
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
        return row

    df = df.apply(extract_json_to_columns, axis=1)

    if 'gender' in df.columns:
        df['gender'] = df['gender'].apply(sanitize_gender)

    if 'country_region_name' in df.columns:
        df['country_region_name'] = df['country_region_name'].apply(standardize_country_name)
    if 'country' in df.columns:
        df['country'] = df['country'].apply(standardize_country_name)

    df = merge_columns(df, 'phone_number', ['phone_number', 'mobile_no', 'mobile_number',
                                            'phone_number_for_cpc_issuance_via_sms', 'phone_number_for_cpd_issuance_via_sms',
                                            'phone', 'mobile', 'the_critical_role_of_in_vitro_dphonenumber'])
    df = merge_columns(df, 'county', ['county___state___region', 'county', 'state_county_district',
                                      'county_state_city_district', 'the_critical_role_of_in_vitro_dstate_county_district'])
    df = merge_columns(df, 'country', ['country_region_name', 'country', 'the_critical_role_of_in_vitro_dcountry'])
    df = merge_columns(df, 'profession', ['profession___cadres', 'cadre', 'cadre__profession', 'profession',
                                          'profession_cadre', 'specialization', 'specilization', 'the_critical_role_of_in_vitro_dprofession'])
    df = merge_columns(df, 'job_title', ['industry_job_title', 'job_title'])
    df = merge_columns(df, 'workplace', ['name_of_the_workplace', 'name_of_equity_afia_working_at_affiliated_with',
                                         'name_of_equity_afia__working_at__affiliated_with', 'name_of_work_place',
                                         'the_critical_role_of_in_vitro_dorganization_affiliation_workplace', 'location'])
    df = merge_columns(df, 'registration_number', ['registration_number', 'registration_no',
                                                   'board_registration_number', 'board_registration_number_compulsory_for_cpd_issuance',
                                                   'board_registration_number_compulsory_for_cpd_issuance_if_not_available_indicate_by_n_a',
                                                   'medical_board_kmpdc__nck__coc__ppb', 'medical_board_number_kmpdc__nck__coc__ppb',
                                                   'registration_license_number', 'registration_number__compulsory_for_cpd_issuance',
                                                   'registration_number_compulsory_for_cpd_issuance', 'registration_practice_number',
                                                   'registration_no2', 'practice__registration_number', 'board_number'])

    fields_to_drop = ['approval_status', 'other_info', 'can_your_email_be_used_for_future_communications',
                      'organisation_affiliation', 'is_guest', 'join_time', 'will_you_require_a_cpd_token_for_this_meeting',
                      'kmpdc_reg_no', 'leave_time', 'organization_affiliation', 'association', 'association_name',
                      'attendee_details', 'branch', 'enrollment_number', 'facility_name', 'institution',
                      'privacy_statement:_we_ensure_any_data_you_provide_is_held_securely_by_supplying_your_contact_information__you_authorize_the_host__and_the_sponsor_of_this_webinar__to_contact_you_with_more_content_and_information_about_products_and_services',
                      'specialty', 'utm_source', '#', 'are_you_a_person_living_with_a_non_communicable_disease_ncd',
                      'organization', 'source_name', 'utm_source', '', 'nan', 'utm_campaign', 'type_of_staff',
                      'designation', 'speciality', 'user_nameoriginal_name_', 'title']
    df.drop(columns=fields_to_drop, inplace=True, errors='ignore')

    # Save transformed file locally and upload to GCS
    df.to_csv(transformed_file, index=False)
    transformed_blob = bucket.blob(f'{entity}_transformed_data_{date_suffix}.csv')
    transformed_blob.upload_from_filename(transformed_file)

postgres_hospital_report_to_gcs = PostgresToGCSOperator(
    task_id='postgres_hospital_report_to_gcs',
    sql="""SELECT 
             o.name AS organization_name,
             e.title AS event_title,
             eu.first_name,
             eu.last_name,
             eu.email,
             ee.duration,
             o.category AS organization_category,
             ee.attended AS attended,
             to_char(ee.enrollment_date, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS registration_time,
             eu.other_info
           FROM public.organization_organization o
           LEFT JOIN public.events_event_specialization s ON o.id = s.event_id
           LEFT JOIN public.events_event e ON o.id = e.organization_id_id
           LEFT JOIN public.event_enrolment_eventenrollment ee ON e.id = ee.event_id_id
           LEFT JOIN public.event_enrolment_eventuser eu ON ee.user_id_id = eu.id
           WHERE o.category='hospital' AND e.title IS NOT NULL""",
    bucket=BQ_BUCKET,
    filename=f'hospital_raw_data_{date_suffix}.csv',
    export_format='csv',
    postgres_conn_id=PG_CON_ID,
    field_delimiter=',',
    gzip=False,
    task_concurrency=1,
    execution_timeout=timedelta(minutes=10),
    gcp_conn_id=BQ_CON_ID,
    dag=dag,
)

postgres_avenue_report_to_gcs = PostgresToGCSOperator(
    task_id='postgres_avenue_report_to_gcs',
    sql="""SELECT 
             o.name AS organization_name,
             e.title AS course_name,
             eu.first_name,
             eu.last_name,
             eu.email,
             ee.duration,
             o.category AS organization_category,
             ee.attended AS attended,
             to_char(ee.enrollment_date, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS registration_time,
             eu.other_info
           FROM public.organization_organization o
           LEFT JOIN public.events_event_specialization s ON o.id = s.event_id
           LEFT JOIN public.events_event e ON o.id = e.organization_id_id
           LEFT JOIN public.event_enrolment_eventenrollment ee ON e.id = ee.event_id_id
           LEFT JOIN public.event_enrolment_eventuser eu ON ee.user_id_id = eu.id
           WHERE o.name='Avenue Healthcare' AND e.title IS NOT NULL AND ee.attended IS NOT NULL""",
    bucket=BQ_BUCKET,
    filename=f'avenue_raw_data_{date_suffix}.csv',
    export_format='csv',
    postgres_conn_id=PG_CON_ID,
    field_delimiter=',',
    gzip=False,
    task_concurrency=1,
    execution_timeout=timedelta(minutes=10),
    gcp_conn_id=BQ_CON_ID,
    dag=dag,
)

postgres_ccare_report_to_gcs = PostgresToGCSOperator(
    task_id='postgres_ccare_report_to_gcs',
    sql="""SELECT 
             o.name AS organization_name,
             e.title AS event_title,
             eu.first_name,
             eu.last_name,
             eu.email,
             ee.duration,
             o.category AS organization_category,
             ee.attended AS attended,
             to_char(ee.enrollment_date, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS registration_time,
             eu.other_info
           FROM public.organization_organization o
           LEFT JOIN public.events_event_specialization s ON o.id = s.event_id
           LEFT JOIN public.events_event e ON o.id = e.organization_id_id
           LEFT JOIN public.event_enrolment_eventenrollment ee ON e.id = ee.event_id_id
           LEFT JOIN public.event_enrolment_eventuser eu ON ee.user_id_id = eu.id
           WHERE o.name='CCARE E-LEARNING PORTAL' AND e.title IS NOT NULL AND ee.attended IS NOT NULL""",
    bucket=BQ_BUCKET,
    filename=f'ccare_raw_data_{date_suffix}.csv',
    export_format='csv',
    postgres_conn_id=PG_CON_ID,
    field_delimiter=',',
    gzip=False,
    task_concurrency=1,
    execution_timeout=timedelta(minutes=10),
    gcp_conn_id=BQ_CON_ID,
    dag=dag,
)

postgres_ngo_report_to_gcs = PostgresToGCSOperator(
    task_id='postgres_ngo_report_to_gcs',
    sql="""SELECT 
             o.name AS organization_name,
             e.title AS event_title,
             eu.first_name,
             eu.last_name,
             eu.email,
             ee.duration,
             o.category AS organization_category,
             ee.attended AS attended,
             to_char(ee.enrollment_date, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS registration_time,
             eu.other_info
           FROM public.organization_organization o
           LEFT JOIN public.events_event_specialization s ON o.id = s.event_id
           LEFT JOIN public.events_event e ON o.id = e.organization_id_id
           LEFT JOIN public.event_enrolment_eventenrollment ee ON e.id = ee.event_id_id
           LEFT JOIN public.event_enrolment_eventuser eu ON ee.user_id_id = eu.id
           WHERE o.category='ngo' AND e.title IS NOT NULL""",
    bucket=BQ_BUCKET,
    filename=f'ngo_raw_data_{date_suffix}.csv',
    export_format='csv',
    postgres_conn_id=PG_CON_ID,
    field_delimiter=',',
    gzip=False,
    task_concurrency=1,
    execution_timeout=timedelta(minutes=10),
    gcp_conn_id=BQ_CON_ID,
    dag=dag,
)

postgres_pharma_report_to_gcs = PostgresToGCSOperator(
    task_id='postgres_pharma_report_to_gcs',
    sql="""SELECT 
             o.name AS organization_name,
             e.title AS event_title,
             eu.first_name,
             eu.last_name,
             eu.email,
             ee.duration,
             o.category AS organization_category,
             ee.attended AS attended,
             to_char(ee.enrollment_date, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS registration_time,
             eu.other_info
           FROM public.organization_organization o
           LEFT JOIN public.events_event_specialization s ON o.id = s.event_id
           LEFT JOIN public.events_event e ON o.id = e.organization_id_id
           LEFT JOIN public.event_enrolment_eventenrollment ee ON e.id = ee.event_id_id
           LEFT JOIN public.event_enrolment_eventuser eu ON ee.user_id_id = eu.id
           WHERE o.category='pharma' AND e.title IS NOT NULL""",
    bucket=BQ_BUCKET,
    filename=f'pharma_raw_data_{date_suffix}.csv',
    export_format='csv',
    postgres_conn_id=PG_CON_ID,
    field_delimiter=',',
    gzip=False,
    task_concurrency=1,
    execution_timeout=timedelta(minutes=10),
    gcp_conn_id=BQ_CON_ID,
    dag=dag,
)

postgres_association_report_to_gcs = PostgresToGCSOperator(
    task_id='postgres_association_report_to_gcs',
    sql="""SELECT 
             o.name AS organization_name,
             e.title AS event_title,
             eu.first_name,
             eu.last_name,
             eu.email,
             ee.duration,
             o.category AS organization_category,
             ee.attended AS attended,
             to_char(ee.enrollment_date, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS registration_time,
             eu.other_info
           FROM public.organization_organization o
           LEFT JOIN public.events_event_specialization s ON o.id = s.event_id
           LEFT JOIN public.events_event e ON o.id = e.organization_id_id
           LEFT JOIN public.event_enrolment_eventenrollment ee ON e.id = ee.event_id_id
           LEFT JOIN public.event_enrolment_eventuser eu ON ee.user_id_id = eu.id
           WHERE o.category='association' AND e.title IS NOT NULL""",
    bucket=BQ_BUCKET,
    filename=f'association_raw_data_{date_suffix}.csv',
    export_format='csv',
    postgres_conn_id=PG_CON_ID,
    field_delimiter=',',
    gzip=False,
    task_concurrency=1,
    execution_timeout=timedelta(minutes=10),
    gcp_conn_id=BQ_CON_ID,
    dag=dag,
)

# Define PythonOperator tasks for transforming data for each entity
transform_hospital_data_task = PythonOperator(
    task_id='transform_hospital_data',
    python_callable=transform_data,
    op_args=['hospital'],
    dag=dag,
)

transform_avenue_data_task = PythonOperator(
    task_id='transform_avenue_data',
    python_callable=transform_data,
    op_args=['avenue'],
    dag=dag,
)

transform_ccare_data_task = PythonOperator(
    task_id='transform_ccare_data',
    python_callable=transform_data,
    op_args=['ccare'],
    dag=dag,
)

transform_ngo_data_task = PythonOperator(
    task_id='transform_ngo_data',
    python_callable=transform_data,
    op_args=['ngo'],
    dag=dag,
)

transform_pharma_data_task = PythonOperator(
    task_id='transform_pharma_data',
    python_callable=transform_data,
    op_args=['pharma'],
    dag=dag,
)

transform_association_data_task = PythonOperator(
    task_id='transform_association_data',
    python_callable=transform_data,
    op_args=['association'],
    dag=dag,
)

load_csv_hospital_data_to_bq = GCSToBigQueryOperator(
    task_id='load_csv_hospital_data_to_bq',
    bucket=BQ_BUCKET,
    source_objects=[f'hospital_transformed_data_{date_suffix}.csv'],
    destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE2}",
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_TRUNCATE',
    gcp_conn_id=BQ_CON_ID,
    max_bad_records=100,
    dag=dag,
)

load_csv_avenue_data_to_bq = GCSToBigQueryOperator(
    task_id='load_csv_avenue_data_to_bq',
    bucket=BQ_BUCKET,
    source_objects=[f'avenue_transformed_data_{date_suffix}.csv'],
    destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE5}",
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_TRUNCATE',
    gcp_conn_id=BQ_CON_ID,
    max_bad_records=100,
    dag=dag,
)

load_csv_ccare_data_to_bq = GCSToBigQueryOperator(
    task_id='load_csv_ccare_data_to_bq',
    bucket=BQ_BUCKET,
    source_objects=[f'ccare_transformed_data_{date_suffix}.csv'],
    destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE6}",
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_TRUNCATE',
    gcp_conn_id=BQ_CON_ID,
    max_bad_records=100,
    dag=dag,
)

load_csv_ngo_data_to_bq = GCSToBigQueryOperator(
    task_id='load_csv_ngo_data_to_bq',
    bucket=BQ_BUCKET,
    source_objects=[f'ngo_transformed_data_{date_suffix}.csv'],
    destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE1}",
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_TRUNCATE',
    gcp_conn_id=BQ_CON_ID,
    max_bad_records=100,
    dag=dag,
)

load_csv_pharma_data_to_bq = GCSToBigQueryOperator(
    task_id='load_csv_pharma_data_to_bq',
    bucket=BQ_BUCKET,
    source_objects=[f'pharma_transformed_data_{date_suffix}.csv'],
    destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE3}",
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_TRUNCATE',
    gcp_conn_id=BQ_CON_ID,
    max_bad_records=100,
    dag=dag,
)

load_csv_association_data_to_bq = GCSToBigQueryOperator(
    task_id='load_csv_association_data_to_bq',
    bucket=BQ_BUCKET,
    source_objects=[f'association_transformed_data_{date_suffix}.csv'],
    destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE4}",
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_TRUNCATE',
    gcp_conn_id=BQ_CON_ID,
    max_bad_records=100,
    dag=dag,
)

# Set task dependencies
postgres_hospital_report_to_gcs >> transform_hospital_data_task >> load_csv_hospital_data_to_bq

postgres_ngo_report_to_gcs >> transform_ngo_data_task >> load_csv_ngo_data_to_bq

postgres_pharma_report_to_gcs >> transform_pharma_data_task >> load_csv_pharma_data_to_bq

postgres_association_report_to_gcs >> transform_association_data_task >> load_csv_association_data_to_bq

postgres_avenue_report_to_gcs >>transform_avenue_data_task >> load_csv_avenue_data_to_bq

postgres_ccare_report_to_gcs >>transform_ccare_data_task >> load_csv_ccare_data_to_bq
