import pandas as pd
from datetime import datetime

costar_export = pd.read_csv('data/raw/costar_export.csv')
master_complist = pd.read_csv('data/raw/master_complist.csv')
hellodata_details = pd.read_csv('data/raw/property_details.csv')
hellodata_costar_ref = pd.read_csv('data/raw/hellodata_costar_ref.csv').rename(columns={'property_id': 'hellodata_id'})
branded_sites = pd.read_csv('data/raw/branded_sites.csv')

final = pd.merge(costar_export, hellodata_costar_ref, left_on='property_id', right_on='costar_id', how='right').dropna(subset='property_id')
final = pd.merge(final, branded_sites[['property_id', 'manager', 'owner']], on='property_id')

final['internal'] = final['hellodata_id'].isin(master_complist.loc[master_complist['comp'] == master_complist['property'], 'hellodata_id'])
final['comp'] = final['hellodata_id'].isin(master_complist['hellodata_id'])

final['building_age'] = (datetime.now().year - final['year_built']).round()

final['year_renovated'] = final['year_renovated'].fillna(final['year_built'])
final['years_since_reno'] = (datetime.now().year - final['year_renovated']).round()

final['years_since_acquisition'] = (datetime.now().year - final['year_acquired']).round()

final.to_csv('data/processed/asset_metrics.csv')
