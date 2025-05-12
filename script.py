import pandas as pd

#Initialize Data

csv_path = "Downloads\\Movie_Data_File.csv"

df = pd.read_csv(csv_path)

#print(df.to_string)
print(df.info)

