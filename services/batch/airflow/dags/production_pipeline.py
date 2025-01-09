from typing import List
import dlt
from sql_database import sql_database



def load_selected_production_tables() -> None:
    # Pipeline for production data
    production_pipeline = dlt.pipeline(pipeline_name='mlh_production', destination='bigquery', dataset_name='mlh_etl_production')

    # Configure the source to load a few select tables incrementally
    production_source = sql_database(credentials=dlt.secrets.get('mlh_production')).with_resources('organization_organization',
                                            'events_event', 
                                            'event_enrolment_eventenrollment', 
                                            'event_enrolment_eventuser')
    

    production_source.organization_organization.apply_hints(incremental=dlt.sources.incremental('updated_at'))
    production_source.events_event.apply_hints(incremental=dlt.sources.incremental('updated_at'))
    production_source.event_enrolment_eventenrollment.apply_hints(incremental=dlt.sources.incremental('updated_at'))
    production_source.event_enrolment_eventuser.apply_hints(incremental=dlt.sources.incremental('updated_at'))
    info = production_pipeline.run(production_source)
    print(info)

#If you need to load the entire database
#It might take time if the database is large
def load_entire_database() -> None:
    """Use the sql_database source to completely load all tables in a database"""
    pipeline = dlt.pipeline(pipeline_name='mlh_production_all_table', destination='bigquery', dataset_name='mlh_etl_production')

    source = sql_database(credentials=dlt.secrets.get('mlh_production'))

    info = pipeline.run(source, write_disposition="replace")
    print(info)



if __name__ == '__main__':
    load_selected_production_tables()
