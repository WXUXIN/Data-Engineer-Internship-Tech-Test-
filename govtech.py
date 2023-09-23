import json
import pandas as pd

# I want to store Restaurant Id
# ◦   	Restaurant Name
# ◦   	Country
# ◦   	City
# ◦   	User Rating Votes
# ◦   	User Aggregate Rating (in float)
# ◦   	Cuisines

# I will have a list containing dictionaries of restaurants with a structure like this:

# rest_id : {
#     "name": "string",
#     "country": "string",
#     "city": "string",
#     "user_rating_votes": "string",
#     "user_aggregate_rating": "string",
#     "cuisines": ["string", "string"]
# }


with open('restaurant_data.json', 'r') as file:
    main_data = json.load(file)

main_rest_lst = []

for outer_dict in main_data:
    
    # Get the list of restaurants using outer_dict['restaurant']
    rest_lst = outer_dict['restaurants']

    # Loop through the list of restaurants, which themselves are dictionaries
    for rest in range(len(rest_lst)):
        rest_data = rest_lst[rest]['restaurant']
        
        # Initialise dict to store restaurant data
        rest_dict = {}

        # For Restaurant Id
        rest_dict['Restaurant Id'] = rest_data.get('R', {}).get('res_id', 'NA')

        # For Restaurant Name
        rest_dict['Restaurant Name'] = rest_data.get('name', 'NA')

        # For User Rating Votes, User Aggregate Rating
        rating_data = rest_data.get('user_rating', {})
        rest_dict['User Rating Votes'] = rating_data.get('votes', 'NA')
        rest_dict['User Aggregate Rating'] = float(rating_data.get('aggregate_rating', 'NA'))

        # For Country and City
        location_data = rest_data.get('location', {})
        rest_dict['Country'] = location_data.get('country_id', 'NA')
        rest_dict['City'] = location_data.get('city', 'NA')

        # For Cuisines
        rest_dict['Cuisines'] = rest_data.get('cuisines', 'NA')

        # Append the restaurant data to the main list
        main_rest_lst.append(rest_dict)

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(main_rest_lst)

# Save the DataFrame to an Excel file
file_name = "restaurants.xlsx"
df.to_excel(file_name, index=False)

print(f"Data saved to {file_name}")

        
