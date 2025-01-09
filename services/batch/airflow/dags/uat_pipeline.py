from typing import List
import dlt
from dlt.common import pendulum
from sql_database import sql_database, sql_table



def load_select_uat_tables() -> None:
    """Use the sql_database source to reflect an entire database schema and load select tables from it.

    This example sources data from the public Rfam MySQL database.
    """
    # Pipeline for uat data
    uat_pipeline = dlt.pipeline(pipeline_name='mlh_uat', destination='bigquery', dataset_name='mlh_etl')

    # Configure the source to load a few select tables incrementally
    uat_source = sql_database(credentials=dlt.secrets.get('mlh_uat')).with_resources('organization_organization',
                                            'events_event', 
                                            'event_enrolment_eventenrollment', 
                                            'event_enrolment_eventuser')
    

    uat_source.organization_organization.apply_hints(incremental=dlt.sources.incremental('updated_at'))
    uat_source.events_event.apply_hints(incremental=dlt.sources.incremental('updated_at'))
    uat_source.event_enrolment_eventenrollment.apply_hints(incremental=dlt.sources.incremental('updated_at'))
    uat_source.event_enrolment_eventuser.apply_hints(incremental=dlt.sources.incremental('updated_at'))
    info = uat_pipeline.run(uat_source)
    print(info)


def load_entire_database() -> None:
    """Use the sql_database source to completely load all tables in a database"""
    pipeline = dlt.pipeline(pipeline_name='mlh_uat', destination='bigquery', dataset_name='mlh_etl')

    source = sql_database()

    info = pipeline.run(source, write_disposition="replace")
    print(info)


def load_standalone_table_resource() -> None:
    """Load a few known tables with the standalone sql_table resource"""
    pipeline = dlt.pipeline(pipeline_name='uat_standalone_sample', destination='bigquery', dataset_name='mlh_etl')

    sample_table_1 = sql_table(
        table='sample_table_1_name',
        incremental=dlt.sources.incremental('updated', initial_value=pendulum.DateTime(2022, 1, 1, 0, 0, 0))
    )

    # Load all data from another table
    sample_table_2 = sql_table(table='sample_table_2_name')

    # Run the resources together
    info = pipeline.extract([sample_table_1, sample_table_2], write_disposition='merge')
    print(info)



if __name__ == '__main__':
    # Load selected tables with different settings
    load_select_uat_tables()

    # Load tables with the standalone table resource
    # load_standalone_table_resource()

    # Load all tables from the database.
    # Warning: The sample database is very large
    # load_entire_database()
