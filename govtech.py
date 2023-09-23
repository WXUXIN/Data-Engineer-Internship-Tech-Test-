import json
import pandas as pd

with open('restarant_data.json') as main_data:
  main_data = main_data.read()


# df_json = pd.read_json('restaurant_data.json')
# print(df_json)




# Print out the keys and values
# for key in parsed_json:
#     print(key + ':', parsed_json[key])

# Loop for rest_data keys and values
# for key in rest_data:
#     print(key + ':') 
#     print("\n")
#     print(rest_data[key])
# # print(parsed_json)

# import json

# with open('restaurant_data.json', 'r') as restaurant_data:
#     restaurant_data = json.load(restaurant_data)
#     print(json.dumps(restaurant_data, indent=4))