import pandas as pd

# Sample list of restaurants
restaurants_lst = [
    {
        "restaurant": {
            "R": {
                "res_id": 18484761
            },
            "apikey": "",
            "name": "rest_name_1",
            "location": {
                "country_id": 1,
                "city": "SomeCity1"
            },
            "user_rating": {
                "votes": 123,
                "aggregate_rating": "4.5"
            },
            "cuisines": "Asian, Italian"
        }
    },
    {
        "restaurant": {
            "R": {
                "res_id": 18484762
            },
            "apikey": "",
            "name": "rest_name_2",
            "location": {
                "country_id": 2,
                "city": "SomeCity2"
            },
            "user_rating": {
                "votes": 456,
                "aggregate_rating": "4.0"
            },
            "cuisines": "French, American"
        }
    }
]

# Convert the list of restaurants into a DataFrame
df = pd.json_normalize([entry['restaurant'] for entry in restaurants_lst])

# Rename columns and select only the desired ones
df = df.rename(columns={
    'R.res_id': 'Restaurant Id',
    'name': 'Restaurant Name',
    'location.country_id': 'Country',
    'location.city': 'City',
    'user_rating.votes': 'User Rating Votes',
    'user_rating.aggregate_rating': 'User Aggregate Rating',
    'cuisines': 'Cuisines'
})
selected_columns = [
    'Restaurant Id',
    'Restaurant Name',
    'Country',
    'City',
    'User Rating Votes',
    'User Aggregate Rating',
    'Cuisines'
]
df = df[selected_columns]

# Convert User Aggregate Rating from string to float
df['User Aggregate Rating'] = df['User Aggregate Rating'].astype(float)

# Save to Excel
df.to_excel('restaurants_data.xlsx', index=False)