import json
import pandas as pd
import datetime
import warnings

# For the first task, this is what I would do:
#
# For each restaurant, I want to store:
# Restaurant Id
# Restaurant Name
# Country
# City
# User Rating Votes
# User Aggregate Rating (in float)
# Cuisines
#
# To do so, I will have a list containing dictionaries of restaurants with a structure like this:
# {
#     "Restaurant Id": "string",
#     "Restaurant Name": "string",
#     "Country": "string",
#     "City": "string",
#     "User Rating Votes": "string",
#     "User Aggregate Rating": "string",
#     "Cuisines": "string"
# }
#
# After extracting the data, I will convert the list of dictionaries to a Pandas DataFrame and save it as a CSV file (restaurants.csv).



# For the second task, this is what I would do:
#
# For each restaurant's event, I want to store:
# Event Id
# Restaurant Id
# Restaurant Name
# Photo URL
# Event Title
# Event Start Date
# Event End Date
#
# To do so, I will have a list containing dictionaries of events for each restaurant with a structure like this:
# {
#         "Restaurant Id": "string",
#         "Restaurant Name": "string",
#         "Photo URL": "string",
#         "Event Title": "string",
#         "Event Start Date": "string",
#         "Event End Date": "string"
# }
# After extracting the data, I will convert the list of dictionaries to a Pandas DataFrame and save it as a CSV file (restaurant_events.csv).



# For the third task, this is what I would do:
#
# I will extract the list of restaurants and their ratings and store the data as restaurant_ratings.csv.
# The structure of the dictionary will be:
# {
#         "Restaurant Name": "string",
#         "Rating Text": "string",
#         "User Aggregate Rating": "float"
# }
#
# I will then convert the list of dictionaries to a Pandas DataFrame
#
# After extracting the data, I will filter the data to only include restaurants with the following ratings:
# Excellent
# Very Good
# Good
# Average
# Poor
#
# I will drop rows without User Aggregate Rating.
#
# I will then group by rating_text and get the minimum and maximum of user_aggregate_rating for each group.
#
# I will then sort the DataFrame by the minimum user_aggregate_rating in descending order, for easier viewing.
#
# Finally I will print out the DataFrame to the console.

def process_data(filename='restaurant_data.json'):
    countries = pd.read_excel('Country-Code.xlsx')

    with open(filename, 'r') as file:
        main_data = json.load(file)

    main_rest_lst = []
    rest_with_event_lst = []
    rating_list = []

    # If the JSON file is empty, raise an exception
    if not main_data:
        raise Exception("JSON file is empty")
    
    
    for outer_dict in main_data:
        
        # Get the list of restaurants using outer_dict['restaurant']
        rest_lst = outer_dict['restaurants']

        # Loop through the list of restaurants, which themselves are dictionaries
        for rest in range(len(rest_lst)):
            
            # Extract the list of restaurants that have past event in 
            # the month of April 2019 and store the data as restaurant_events.csv.

            rest_data = rest_lst[rest]['restaurant']
            location_data = rest_data.get('location', {})
            rating_data = rest_data.get('user_rating', {})
            
            rest_dict = {
                "Restaurant Id": rest_data.get('R', {}).get('res_id', 'NA'),
                "Restaurant Name": rest_data.get('name', 'NA'),
                "User Rating Votes": rating_data.get('votes', 'NA'),
                "User Aggregate Rating": float(rating_data.get('aggregate_rating', 'NA')),
                "Cuisines": rest_data.get('cuisines', 'NA'),
                "Country": location_data.get('country_id', 'NA'),
                "City": location_data.get('city', 'NA')
            }

            # Append the restaurant data to the main list
            main_rest_lst.append(rest_dict)

            zomato_events = rest_data.get('zomato_events', [])

            for event_data in zomato_events:
                event = event_data.get('event', {})
                
                # If we get an empty event, skip this event
                if not event:
                    continue

                start_date = event.get("start_date", None)

                # If we get an empty start date, skip this event
                if not start_date:
                    continue

                # This is assuming that the date is in the format YYYY-MM-DD, 
                start_date = datetime.datetime.strptime(event["start_date"], "%Y-%m-%d").date()

                # Check if the event was active in April 2019
                if start_date <= datetime.date(2019, 4, 30) and start_date >= datetime.date(2019, 4, 1):
                    
                    # First check is to check if there are any photos
                    photo_urls = event["photos"] if event["photos"] else "NA"

                    # Second is to check for each photo dictionary, if there is a url key
                    # If there is, extract the url, else, replace it with NA
                    if photo_urls != "NA":
                        photo_urls = [photo["photo"]["url"] if photo.get("photo", {}).get("url", None) else "NA" for photo in event["photos"]]
                    
                    event_info = {
                        "Event Id": event["event_id"],
                        "Restaurant Id": rest_data.get('R', {}).get('res_id', 'NA'),
                        "Restaurant Name": rest_data.get('name', 'NA'),
                        "Photo URL": photo_urls,
                        "Event Title": event["title"],
                        "Event Start Date": event["start_date"],
                        "Event End Date": event["end_date"]
                    }
                    
                    rest_with_event_lst.append(event_info)

            rating_data = rest_data.get('user_rating', {})
            rating_text = rating_data.get('rating_text', 'NA')
            aggregate_rating = float(rating_data.get('aggregate_rating', 'NA'))
            rating_list.append({
                'Restaurant Name': rest_data.get('name', 'NA'),
                'Rating Text': rating_text,
                'User Aggregate Rating': aggregate_rating
            })
                
    # Convert the list of dictionaries to a Pandas DataFrame
    main_df = pd.DataFrame(main_rest_lst)
    rest_with_event_df = pd.DataFrame(rest_with_event_lst)
    rating_df = pd.DataFrame(rating_list)

    # Explode the Photo URL column so that each row contains only one URL
    rest_with_event_df_exploded = rest_with_event_df.explode('Photo URL').reset_index(drop=True)

    # I want to merge countries witht the DataFrame, using the country_id as the key
    main_df = pd.merge(main_df, countries, how='left', left_on='Country', right_on='Country Code')

    # If there are restaurants with country code not in the excel sheet provided, and city is not dummy, raise exception
    if main_df[main_df['Country Code'].isna() & (main_df['City'] != 'Dummy')].shape[0] > 0:
        warnings.warn(f"Invalid country code detected!")
    
    # main_df = main_df.dropx(['Country_x', 'Country Code'], axis=1)
    # Rename the column to Country
    main_df = main_df.rename(columns={'Country_y': 'Country'})

    # Reorder the columns
    main_df = main_df[[
        'Restaurant Id',
        'Restaurant Name',
        'Country',
        'City',
        'User Rating Votes',
        'User Aggregate Rating',
        'Cuisines'
    ]]

    # If any value is NA, replace it with 'NA'
    main_df = main_df.fillna('NA')

    # Save the DataFrame to an Excel file
    main_df.to_csv('restaurants.csv', index=False)
    rest_with_event_df_exploded.to_csv('restaurant_events.csv', index=False)

    # Filter only required ratings
    required_ratings = ['Excellent', 'Very Good', 'Good', 'Average', 'Poor']
    rating_df = rating_df[rating_df['Rating Text'].isin(required_ratings)]

    # Drop rows without User Aggregate Rating
    rating_df = rating_df[rating_df['User Aggregate Rating'] != 'NA']

    # Group by Rating Text and then get the minimum and maximum of User Aggregate Rating for each group
    grouped = rating_df.groupby('Rating Text')['User Aggregate Rating'].agg(['min', 'max'])

    # Sort by the minimum User Aggregate Rating
    grouped = grouped.sort_values(by='min', ascending=False)

    print("\nThreshold for the different rating text: \n")
    print(f"{grouped} \n")

    print("Data saved!\n")

if __name__ == "__main__":
    process_data()

            
