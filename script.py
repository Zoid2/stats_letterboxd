import pandas as pd
import ast
import json

#Initialize Data

csv_path = "Movie_Data_File.csv"

df = pd.read_csv(csv_path)

#print(df.to_string)
# print(df.info)
# print(df["Film_title"])




# Drop rows where Countries or Genres is missing
df = df.dropna(subset=['Countries', 'Genres', "Average_rating"])

# Convert stringified lists to actual Python lists
df['Countries'] = df['Countries'].apply(ast.literal_eval)
df['Genres'] = df['Genres'].apply(ast.literal_eval)

# Explode both columns to get all combinations
df_exploded = df.explode('Countries').explode('Genres').explode("Average_rating")

# Keep only the relevant columns
country_genre_df = df_exploded[['Countries', 'Genres', "Average_rating"]].rename(columns={'Countries': 'Country', 'Genres': 'Genre', "Average_rating": "Rating (Avg)"})

# Optional: remove whitespace and duplicates
country_genre_df['Country'] = country_genre_df['Country'].str.strip()
country_genre_df['Genre'] = country_genre_df['Genre'].str.strip()
country_genre_df = country_genre_df.drop_duplicates()

avg_ratings = country_genre_df.groupby(['Country', 'Genre'])['Rating (Avg)'].mean().round(2).reset_index()
avg_ratings_json_data = json.dumps(avg_ratings.to_dict(orient="records"), indent=2)
# print(json_data)
# with open("averageRatingInter.json", "w") as file:
#     file.write(avg_ratings_json_data)

region_map = {
    # North America
    'USA': 'North America',
    'Canada': 'North America',
    'Mexico': 'North America',

    # South America
    'Brazil': 'South America',
    'Argentina': 'South America',
    'Chile': 'South America',

    # Europe
    'UK': 'Europe',
    'France': 'Europe',
    'Germany': 'Europe',
    'Italy': 'Europe',
    'Spain': 'Europe',
    'Netherlands': 'Europe',
    'Sweden': 'Europe',
    'Norway': 'Europe',
    'Denmark': 'Europe',
    'Austria': 'Europe',
    'Belgium': 'Europe',
    'Greece': 'Europe',
    'Hungary': 'Europe',
    'Ireland': 'Europe',

    # Asia
    'India': 'Asia',
    'China': 'Asia',
    'Japan': 'Asia',
    'South Korea': 'Asia',
    'Indonesia': 'Asia',
    'Taiwan': 'Asia',
    'Thailand': 'Asia',
    'Philippines': 'Asia',

    # Middle East
    'United Arab Emirates': 'Middle East',
    'Saudi Arabia': 'Middle East',
    'Turkey': 'Middle East',
    'Israel': 'Middle East',
    'Qatar': 'Middle East',

    # Africa
    'Nigeria': 'Africa',
    'South Africa': 'Africa',
    'Egypt': 'Africa',
    'Kenya': 'Africa',

    # Oceania
    'Australia': 'Oceania',
    'New Zealand': 'Oceania'
}

country_genre_df['Region'] = country_genre_df['Country'].map(region_map)
region_genre_ratings = country_genre_df.groupby(['Region', 'Genre'])['Rating (Avg)'].mean().round(2).reset_index()
# Pivot for plotting (Regions as rows, Genres as columns)
pivot_df = region_genre_ratings.pivot(index='Region', columns='Genre', values='Rating (Avg)').fillna(0)
pivot_df = pivot_df.reset_index()
avg_ratings_reg_json_data = json.dumps(pivot_df.to_dict(orient="records"), indent=2)
region_mean = region_genre_ratings["Rating (Avg)"].mean().round(2)
region_median = region_genre_ratings["Rating (Avg)"].median().round(2)
region_std = region_genre_ratings["Rating (Avg)"].std().round(2)
print(f"Region -- Mean: {region_mean}, Median: {region_median}, Std: {region_std}")

# with open("averageRatingReg.json", "w") as file:
#     file.write(avg_ratings_reg_json_data)

five_star_ratings = df.dropna(subset=["Genres", "★★★★★"])
five_star_ratings = five_star_ratings.explode("Genres")
five_star_ratings['Genres'] = five_star_ratings['Genres'].str.strip()
five_star_ratings = five_star_ratings[["Genres", "★★★★★"]].rename(columns={"Genres": 'Genre', "★★★★★": "Rating (5 Stars)"})
five_star_ratings = five_star_ratings.groupby("Genre", as_index=False).sum()
five_star_mean = five_star_ratings["Rating (5 Stars)"].mean().round(2)
five_star_median = five_star_ratings["Rating (5 Stars)"].median().round(2)
five_star_std = five_star_ratings["Rating (5 Stars)"].std().round(2)
print(f"Five Star -- Mean: {five_star_mean}, Median: {five_star_median}, Std: {five_star_std}")
# print(five_star_ratings)
# with open("five_star_ratings.json", "w") as file:
#     file.write(five_star_ratings.to_json(orient="records", indent=2))


#print(df.head())
#print(country_genre_df.head())
#print(avg_ratings.sort_values(by="Rating (Avg)", ascending=False))
#print(pivot_df.head())
#print(avg_ratings_reg_json_data)
