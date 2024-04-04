import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read GDP data
gdps = pd.read_csv("gdp_data/aaa20012017gdp.csv")
gdps = gdps.transpose()
gdps = gdps.iloc[1:]
gdps.reset_index(inplace=True)
gdps.columns = ['Year'] + list(gdps.iloc[0][1:])
gdps['Year'] = gdps['Year'].astype(int)

# Read production data
production = pd.read_csv("data/Energy Data - Production.csv")
production = production.rename(columns={'YYYYMM': 'Year'})
production['Year'] = production['Year'].astype(str)
production['Value'] = pd.to_numeric(production['Value'], errors='coerce')

# Filter production data to exclude 2006 and 2011
production = production[(production['Year'].str[:4].astype(int) >= 2001) &
                        (production['Year'].str[:4].astype(int) <= 2017) &
                        ~(production['Year'].str[:4].astype(int).isin([2006, 2011]))]

# Aggregate production data by summing up values for each year
agg_production = production.groupby(production['Year'].str[:4].astype(int))['Value'].sum()
agg_production = agg_production.reset_index()
agg_production['Year'] = agg_production['Year'].astype(int)

# Convert 'Year' column to int64 to match the data type in gdps DataFrame
gdps['Year'] = gdps['Year'].astype(int)

# Merge aggregated production data with GDP data on 'Year'
merged = pd.merge(agg_production, gdps, on='Year')

# Read national GDP data
national_gdp = pd.read_csv("gdp_data/natgdp.csv")
national_gdp.columns = ['Year', 'National GDP']
national_gdp['National GDP'] = pd.to_numeric(national_gdp['National GDP'].str.replace(',', ''), errors='coerce') * 1e3

# Merge national GDP data with existing DataFrame
merged = pd.merge(merged, national_gdp, on='Year')

# Plotting
# Plotting
# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(merged['Value'], merged['National GDP'],  label='National GDP', color='blue')
plt.scatter(merged['Value'], merged['3,481'],  label='Abilene, TX GDP', color='red')
plt.scatter(merged['Value'], merged['20,729'],  label='Akron, OH GDP', color='green')
plt.scatter(merged['Value'], merged['3,986'],  label='Albany, GA GDP', color='orange')
plt.xscale('log')  # Set x-axis to logarithmic scale
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.title('Production Value vs GDP')
plt.xlabel('Production Value')
plt.ylabel('GDP in millions')
plt.legend()
plt.grid(True)
plt.show()

