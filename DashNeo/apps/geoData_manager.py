import pandas as pd
from datetime import datetime, timedelta
import yaml
from neo4j.time import DateTime

import neoCypher_manager

envFactor_list = ['temperature', 'precipitation', 'relative_humidity', 'specific_humidity', 'sky_shortwave_irradiance',
                  'wind_speed_10meters_range', 'wind_speed_50meters_range']
# (1) have accession list get location, collection_date, put all the results in a dataframe


def get_day_location():
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    seq_lt = config['seqinfo']['accession_lt']
    # print(len(seq_lt))
    data_type = config['params']['data_type']
    if data_type == 'dna':
        df_day_location = neoCypher_manager.get_dfDayLocation(
            'Nucleotide', seq_lt)
    else:
        df_day_location = neoCypher_manager.get_dfDayLocation(
            'Protein', seq_lt)
    # df_day_location.set_index('id', inplace=True)
    df_day_location['collection_date'] = df_day_location['collection_date'].apply(
        lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
    )
    # df_day_location['collection_date'] = df_day_location['collection_date'].apply(
    #     lambda x: x.to_native())
    # df_day_location['collection_date'] = pd.to_datetime(
    #     df_day_location['collection_date']).dt.date
    return df_day_location

# (2)  Function to generate climate information


def get_climate_info(row):
    location = row['location']
    date = row['collection_date'].strftime('%Y-%m-%d')

    df = neoCypher_manager.get_geoOneDay(location, date)
    geo_dict = {col: df[col] for col in df.columns.tolist()}
    return geo_dict


# Get the df_day_location DataFrame
df_day_location = get_day_location()

# Apply the function to each row of df_day_location and update the DataFrame with climate information
df_day_location['climate_info'] = df_day_location.apply(
    lambda row: get_climate_info(row), axis=1)
# Extract keys from the first row of the climate_info column
keys = df_day_location['climate_info'].iloc[0].keys()

# Create new columns for each key and extract the corresponding values
for key in keys:
    df_day_location[key] = df_day_location['climate_info'].apply(
        lambda x: x.get(key))

# Drop the original climate_info column
df_day_location.drop('climate_info', axis=1, inplace=True)

print(df_day_location)
