from utils import get_data, pre_process
import pandas as pd
from time import time
from colorama import init, Fore
from datetime import datetime
import os


# client_data = get_data.GetClientData()
# Call the retrieve_data method with caching enabled
# df = client_data.retrieve_data(use_cache=True)

# merge data from different API(endpoints) into a single dataframe. This is done by merging on the idMember column

formatted_date = datetime.now().strftime("%Y-%m-%d")
base_path = 'C:\\Users\\Pichau\\PycharmProjects\\worldgym\\data'
destination_path = os.path.join(base_path, formatted_date)
if not os.path.exists(destination_path):
    os.makedirs(destination_path)


print("etapa 1 - merge data")
start_time = time()
members_data_itapoa = get_data.GetClientData(endpoint="/api/v1/members", take_number=150, unidade="itapoa")
df_members = members_data_itapoa.retrieve_data(use_cache=False)
df_members.to_csv(os.path.join(destination_path, f'data_raw_{members_data_itapoa.unidade}.csv'), index=True, header=True)
print(f"df_members_itapoa shape is : {df_members.shape}")

# members_data_planaltina = get_data.GetClientData(endpoint="/api/v1/members", take_number=50, unidade="planaltina")
# df_members_planaltina = members_data_planaltina.retrieve_data(use_cache=False)
# print(f"df_members_planaltina shape is : {df_members_planaltina.shape}")

# df = pd.merge(df_members, df_membership, on="idMember", how="left")
df = df_members
print(f"final df shape is : {df.shape}")
print(df.columns)
# df = df.iloc[ :15, : ]


gym_cordinates = {
    'itapoa': (-15.751971192888982, -47.76314034147339),
    'planaltina': (-15.453192773567416, -47.60772964591448)
}
map_name = {
    'BRASÍLIA': 'Brasilia',
    'BRASILIA': 'Brasilia',
    "'BRASILIA": 'Brasilia',
    ' BRASILIA': 'Brasilia',
    'Brasilia ': 'Brasilia',
    'BARSILIA': 'Brasilia',
    'BRASILI': 'Brasilia',
    'BRASÍLIA-DF': 'Brasilia',
    'BSB': 'Brasilia',
    'Brasilia': 'Brasilia',
    'PLANALTINA': 'Planaltina',
    'PLANALTINA ': 'Planaltina',
    'SOBRADINHO': 'Sobradinho',
    'SOBRADINHO DOS MELOS': 'Sobradinho',
    'GOIÂNIA': 'Goiania',
    'Goiânia': 'Goiania',
    'APARECIDA DE GOIÂNIA': 'Goiania',
    'ITAPOA': 'Itapoa',
    'ITAPOÃ': 'Itapoa',
    'ITAPUÃ': 'Itapoa',
    'ITAPOÃ ': 'Itapoa',
    'ITAPOA-DF ': 'Itapoa',
    'ITAPOA ': 'Itapoa',
    'FAZENDINHA (ITAPOÃ)': 'Itapoa',
    'RIO DE JANEIRO': 'Rio de Janeiro',
    'SÃO PAULO': 'São Paulo',
    'CURITIBA': 'Curitiba',
    'MANAUS': 'Manaus',
    'FORTALEZA': 'Fortaleza',
    'NATAL': 'Natal',
    # Add more name variations here...
}
end_time = time()
elapsed_time = end_time - start_time
print(Fore.GREEN + f"Tempo de execução da etapa 1: {elapsed_time:.2f} segundos")


print("etapa 2 - standarize text data")
start_time = time()
df.loc[ :, 'unidade' ] = members_data_itapoa.unidade
df['city'] = df['unidade'].str.lower().str.strip().str.title()
df = pre_process.apply_map(df, 'city', map_name=map_name)
df[ 'address' ] = df[ 'address' ].fillna('')
df[ 'city' ] = df[ 'city' ].fillna('')
end_time = time()
elapsed_time = end_time - start_time
print(Fore.GREEN + f"Tempo de execução da etapa 2: {elapsed_time:.2f} segundos")

print("etapa 3 - get coordinates from address")
start_time = time()
df[ 'coordinates' ] = (df[ 'address' ] + ', ' + df[ 'city' ]).apply(pre_process.get_coord)
df['gym_coordinates'] = df['unidade'].map(gym_cordinates)
end_time = time()
elapsed_time = end_time - start_time
print(Fore.GREEN + f"Tempo de execução da etapa 3: {elapsed_time:.2f} segundos")

print("etapa 4 - calculate distance")
start_time = time()
df[ 'dist' ] = pre_process.calculate_distance_list(df['coordinates'], df['gym_coordinates'])
end_time = time()
elapsed_time = end_time - start_time
print(Fore.GREEN + f"Tempo de execução da etapa 4: {elapsed_time:.2f} segundos")

print("etapa 5 - get coordinates from zipCode")
start_time = time()
mask = df[ 'dist' ] > 150
df["shortzip"] = df["zipCode"].astype(str).str.slice(start=0, stop=5)
df.loc[mask, 'coordinates'] = df.loc[mask, 'shortzip'].apply(pre_process.get_coordinates_from_cep)
end_time = time()
elapsed_time = end_time - start_time
print(Fore.GREEN + f"Tempo de execução da etapa 5: {elapsed_time:.2f} segundos")


print("etapa 6 - find similar distance")
start_time = time()
nan_mask = df[ 'dist' ].isna()
df.loc[ mask, 'dist' ] = df.loc[ mask, 'zipCode' ].apply(lambda zipCode: pre_process.find_similar_dist(zipCode, df))
df.loc[nan_mask, 'dist'] = df.loc[nan_mask, 'zipCode'].apply(lambda zipCode: pre_process.find_similar_dist(zipCode, df))
end_time = time()
elapsed_time = end_time - start_time
print(f'Numero de nan na coluna dist : {df[ "dist" ].isna().sum()}')
print(Fore.GREEN + f"Tempo de execução da etapa 6: {elapsed_time:.2f} segundos")

print("etapa 7 - create column date_since_last_access")
start_time = time()
df.loc[:, 'lastAccessDate'] = pd.to_datetime(df['lastAccessDate'], errors='coerce')
today = pd.Timestamp(datetime.now().date())
valid_timestamp_mask = df['lastAccessDate'].apply(lambda x: isinstance(x, pd.Timestamp)) # Mask for rows where lastAccessDate is a valid timestamp
df.loc[valid_timestamp_mask, 'date_since_last_access'] = (today - df.loc[valid_timestamp_mask, 'lastAccessDate'])
df['date_since_last_access'] = pd.to_timedelta(df['date_since_last_access']).dt.days
print(df['date_since_last_access'].describe())
print(f'Numero de NaT na coluna dist : {df[ "lastAccessDate" ].isna().sum()}')
print(Fore.GREEN + f"Tempo de execução da etapa 7: {elapsed_time:.2f} segundos")


print(df.shape)
print(df.columns)

# pep 8
print("etapa 8 - save file as data_raw.csv inside data folder")
data = df.copy()
# data['distance'] = pre_process.calculate_distance_list(data['address'], data['unidade'])
data.to_csv(os.path.join(destination_path, f'dataset_{members_data_itapoa.unidade}.csv'), index=True, header=True)
print(Fore.GREEN + "file saved as dataset_{members_data_itapoa.unidade}.csv inside data folder")
