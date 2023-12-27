import numpy as np                                  # import numpy for working with arrays
import pandas as pd                                 # import for working with data sets
import plotly.express as px                         # import for interactive visualization of graphs
pd.set_option('display.float_format', lambda x: '%.2f' % x)       # determine the behaviour of mantissa denotion

population_url='https://raw.githubusercontent.com/ArijitDhali/PrepInsta-DA-Week-4/main/country_population.csv'
population=pd.read_csv(population_url,encoding='unicode_escape')        # reads population dataset
fertility_url='https://raw.githubusercontent.com/ArijitDhali/PrepInsta-DA-Week-4/main/fertility_rate.csv'
fertility=pd.read_csv(fertility_url,encoding='unicode_escape')          # reads fertility rate dataset
metadata_url='https://raw.githubusercontent.com/ArijitDhali/PrepInsta-DA-Week-4/main/metadata_country.csv'
metadata=pd.read_csv(metadata_url,encoding='unicode_escape')            # reads life expectancy dataset
expectancy_url='https://raw.githubusercontent.com/ArijitDhali/PrepInsta-DA-Week-4/main/life_expectancy.csv'
expectancy=pd.read_csv(expectancy_url,encoding='unicode_escape')        # reads metadata dataset

columns_to_remove = ['Indicator Name', 'Indicator Code']                  # variable to store list of unnecessary columns
population = population.drop(columns=columns_to_remove)                   # dropping the unnecessary columns
population.rename(columns={'ï»¿"Country Name"': 'Country Name'}, inplace=True)    # renaming the column header
population = population[population['Country Name'] != 'Not classified']           # filtering out the specific row
population.columns=population.columns.str.lower().str.replace(' ','_')            # standardizing the column header
population.iloc[:, 2:] = population.iloc[:, 2:].apply(lambda row: row.fillna(row.median()), axis=1)   # replacing the NaN values with median of row

columns_to_remove = ['Indicator Name', 'Indicator Code']        # variable to store list of unnecessary columns
fertility = fertility.drop(columns=columns_to_remove)           # dropping the unnecessary columns
fertility.rename(columns={'ï»¿"Country Name"': 'Country Name'}, inplace=True)   # renaming the column header
fertility = fertility[fertility['Country Name'] != 'Not classified']            # filtering out the specific row
fertility.columns=fertility.columns.str.lower().str.replace(' ','_')            # standardizing the column header

columns_to_remove = ['Indicator Name', 'Indicator Code']           # variable to store list of unnecessary columns
expectancy = expectancy.drop(columns=columns_to_remove)            # dropping the unnecessary columns
expectancy.rename(columns={'ï»¿"Country Name"': 'Country Name'}, inplace=True)  # renaming the column header
expectancy = expectancy[expectancy['Country Name'] != 'Not classified']         # filtering out the specific row
expectancy.columns=expectancy.columns.str.lower().str.replace(' ','_')          # standardizing the column header

columns_to_remove = ['SpecialNotes', 'Unnamed: 5']          # variable to store list of unnecessary columns
metadata = metadata.drop(columns=columns_to_remove)         # dropping the unnecessary columns
metadata.rename(columns={'ï»¿"Country Code"': 'Country Code'}, inplace=True)    # renaming the column header
metadata.rename(columns={'IncomeGroup': 'Income Group'}, inplace=True)          # renaming the column header
metadata.rename(columns={'TableName': 'Country Name'}, inplace=True)            # renaming the column header
column_to_shift = metadata.pop(metadata.columns[3])           # shifting column 3 to 0
metadata.insert(0, column_to_shift.name, column_to_shift)
metadata.columns=metadata.columns.str.lower().str.replace(' ','_')              # standardizing the column header

columns_to_merge = ['country_name','region']    # listing the column headers required after merging

population_metadata = population.merge(metadata[columns_to_merge], on='country_name')    # merge at country_name
column_to_shift = population_metadata.pop(population_metadata.columns[-1])               # shifting columns
population_metadata.insert(2, column_to_shift.name, column_to_shift)
melted_data_population = population_metadata.melt(id_vars=['country_name', 'country_code','region'], var_name='year', value_name='population')
sorted_data_population = melted_data_population.sort_values(by=['country_name','year']) # melting, restructuring and sorting data of population

melted_data_fertility = fertility.melt(id_vars=['country_name','country_code'], var_name='year', value_name='fertility')
sorted_data_fertility = melted_data_fertility.sort_values(by=['country_name','year'])       # melting, restructuring and sorting data of population
columns_to_merge = ['fertility','country_name','year']  # listing the column headers required after merging
# merge at country_name and year
population_fertility = sorted_data_population.merge(sorted_data_fertility[columns_to_merge], on=['country_name','year'])

melted_data_expectancy = expectancy.melt(id_vars=['country_name','country_code'], var_name='year', value_name='expectancy')
sorted_data_expectancy = melted_data_expectancy.sort_values(by=['country_name','year'])       # melting, restructuring and sorting data of population
columns_to_merge = ['expectancy','country_name','year']         # listing the column headers required after merging
# merge at country_name and year
final = population_fertility.merge(sorted_data_expectancy[columns_to_merge], on=['country_name','year'])

final.dropna(subset=['region'], inplace=True)               # replace NaN values with 'World'
final['fertility'] = final['fertility'].round(decimals=2)       # round the floating values to 2 decimals
final['expectancy'] = final['expectancy'].round(decimals=2)
final["year"] = final["year"].astype(int)                       # convert the year to integer data type
final.dropna(subset=['population'], inplace=True) # fill missing 'population' values with a default value like 0
final['population'].fillna(0, inplace=True)


fig_fertility_expectation_region = px.scatter(data_frame=final,
                 x='fertility',                    # x-axis consists of fertility
                 y='expectancy',                   # x-axis
                 size='population',                # bubble size based on population
                 size_max=50,                      # set the maximum size for bubbles
                 hover_name='country_name',        # will view country names on hovering
                 color='region',             # will color accordingly to countries
                 animation_frame='year',           # will animate in time frame
                 animation_group='country_name',   # animation format
                 template='plotly_dark',           # black as template
                 range_x=[0, 10],                   # range of x axis
                 range_y=[10, 90])                 # range of y axis

fig_fertility_expectation_region.update_layout(title='Fertility Rate vs. Life Expectancy',                    # title of graph
                  xaxis_title='Fertility Rate - Total [Births per Woman]',  # x label
                  yaxis_title='Life Expectancy at Birth - Total')           # y label

fig_fertility_expectation_region.show()
