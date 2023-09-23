import json
import pandas as pd
import datetime

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

#       Event Id
# ◦   	Restaurant Id
# ◦   	Restaurant Name
# ◦   	Photo URL
# ◦   	Event Title
# ◦   	Event Start Date
# ◦   	Event End Date


countries = pd.read_excel('Country-Code.xlsx')

with open('restaurant_data.json', 'r') as file:
    main_data = json.load(file)

main_rest_lst = []
rest_with_event_lst = []

for outer_dict in main_data:
    
    # Get the list of restaurants using outer_dict['restaurant']
    rest_lst = outer_dict['restaurants']

    # Loop through the list of restaurants, which themselves are dictionaries
    for rest in range(len(rest_lst)):
        
        # Extract the list of restaurants that have past event in 
        # the month of April 2019 and store the data as restaurant_events.csv.

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

        # Check if there have been events in the past, escpecially in April 2019
        # If there are, store the data in a dictionary of the form:
        # {
        #         "event id": 
        #         "restaurant_name": "string",
        #         "photo_url": "string",
        #         "event_title": "string",
        #         "event_start_date": "string",
        #         "event_end_date": "string"
        # }
        # Get the list of events using rest_data['events']

        zomato_events = rest_data.get('zomato_events', [])

        for event_data in zomato_events:
          event = event_data["event"]
          start_date = datetime.datetime.strptime(event["start_date"], "%Y-%m-%d").date()
          end_date = datetime.datetime.strptime(event["end_date"], "%Y-%m-%d").date()
          
          # Check if the event was active in April 2019
          if start_date <= datetime.date(2019, 4, 30) and start_date >= datetime.date(2019, 4, 1):
              
              # Extract all photo URLs
              photo_urls = [photo["photo"]["url"] for photo in event["photos"]] if event["photos"] else "NA"
              
              event_info = {
                  "Event Id": event["event_id"],
                  # For demonstration purposes, I've added a placeholder restaurant name,
                  # but you'll need to extract this from the actual data structure.
                  "Restaurant Id": rest_data.get('R', {}).get('res_id', 'NA'),
                  "Restaurant Name": rest_data.get('name', 'NA'),
                  "Photo URL": photo_urls,
                  "Event Title": event["title"],
                  "Event Start Date": event["start_date"],
                  "Event End Date": event["end_date"]
              }
              
              rest_with_event_lst.append(event_info)
            
# Convert the list of dictionaries to a Pandas DataFrame
main_df = pd.DataFrame(main_rest_lst)
rest_with_event_lst = pd.DataFrame(rest_with_event_lst)

# Explode the Photo URL column so that each row contains only one URL
rest_with_event_lst_exploded = rest_with_event_lst.explode('Photo URL').reset_index(drop=True)

# I want to merge countries witht the DataFrame, using the country_id as the key
main_df = pd.merge(main_df, countries, how='left', left_on='Country', right_on='Country Code')
main_df = main_df.drop(['Country_x', 'Country Code'], axis=1)
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

# Save the DataFrame to an Excel file
main_df.to_csv('restaurants.csv', index=False)
rest_with_event_lst_exploded.to_csv('restaurant_events.csv', index=False)

print("Data saved!")

        
