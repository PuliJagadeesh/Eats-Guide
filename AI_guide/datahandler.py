# this file is to clean, impute and analyse the data.
import pandas as pd


file_path = 'D:/Projects/Liminal/AI_Guide/resources/restaurants_1.csv'  #

#df = pd.read_csv(file_path)

df = pd.read_csv(file_path, na_values=['N/A', 'na', 'NA', 'None', ''])

print("\nDataFrame Information:")
print(df.info())
print("\nSummary Statistics for Numerical Columns:")
print(df.describe())
# Check for missing values in each column
missing_values = df.isnull().sum()

# Display the missing values count for each column
print("Missing values in each column:")
print(missing_values)

print(df['City'].value_counts())