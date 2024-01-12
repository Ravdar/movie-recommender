import json

# Load the JSON data from the original file
with open('movies_db.json', 'r') as json_file:
    data = json.load(json_file)

# Create a new list with the desired fields
filtered_data = [
    {
        'title': entry['fields']['title'],
        'year': entry['fields']['year'],
        'netflix': entry['fields']['netflix'],
        'amazon_prime': entry['fields']['amazon_prime'],
        'disney_plus': entry['fields']['disney_plus'],
        'hulu': entry['fields']['hulu'],
        'hbo_max': entry['fields']['hbo_max'],
        'apple_tv': entry['fields']['apple_tv'],
        'peacock': entry['fields']['peacock'],
    }
    for entry in data
]

# Save the filtered data to a new file
with open('filtered_movies_db.json', 'w') as json_file:
    json.dump(filtered_data, json_file, indent=2)