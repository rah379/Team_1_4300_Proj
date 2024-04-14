import json


def print_lengths_of_items(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    a = 0
    for key in data.keys():
        if len(data[key]) > 0:
            a += 1
            print(f"Length of item '{key}': {len(data[key])}")
    print(a)


# json_file = 'us_list_unfiltered.json'

irrelevant = [
    "Real America's Voice (RAV)",
    "House Foreign Affairs Committee Majority",
    "Armed Services GOP",
    "House Admin. Committee GOP",
    "House Appropriations",
    "House Republicans",
    "Western Caucus",
    "NEWSMAX",
    "Ways and Means Committee",
    "House Democrats",
    "Financial Services GOP",
    "FreedomWorks",
    "House Judiciary GOP",
    "New Democrat Coalition (NDC)",
    "The Hill",
    "Energy & Commerce Democrats",
    "CDC",
    "The White House",
    "The Black Caucus",
    "House Judiciary Dems",
    "Progressive Caucus",
    "House Intelligence Committee",
    "Select Subcommittee on the Coronavirus Pandemic",
    "Oversight Committee",
    "Ways and Means Democrats",
    "Meet the Press",
    "Joint Economic Committee Republicans",
    "House Budget GOP",
    "CAPAC",
    "West Virginia Courts",
    "Senate Republicans",
    "Yellowhammer News",
    "NC Museum of History",
    "House Committee on Agriculture",
    "Energy and Commerce Committee",
    "SenateEnergyDems",
    "California Governor's Office of Emergency Services",
    "Senate Commerce, Science, Transportation Committee",
    "Senate Ag Committee Republicans",
    "Gregory",
]

duplicates = {
    "Rep. Ilhan Omar": "Ilhan Omar",
    "Vice President Kamala Harris": "Kamala Harris",
    "DeSantis War Room": "Ron DeSantis",
    "Congressman Greg Steube": "Greg Steube",
}


def remove_keys_from_json(json_file, irrelevant_indices):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Check if data is a dictionary
    if isinstance(data, dict):
        for index in irrelevant_indices:
            # Remove the key at the specified index
            if index in data:
                del data[index]
    else:
        print("Data structure is not a dictionary.")

    # Write the modified data back to the JSON file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)


json_file = 'data/tweets/raw.json'
irrelevant_indices = irrelevant  # List of keys to remove
remove_keys_from_json(json_file, irrelevant_indices)


def remove_keys_with_few_instances(json_file, output, min_instances=10):
    with open(json_file, 'r') as f:
        data = json.load(f)

    entry_counts = {}
    for entry in data:
        entry_counts[entry] = len(data[entry])
    # print(entry_counts)

    # Remove entries with counts below the threshold
    for key in entry_counts.keys():
        if entry_counts[key] <= min_instances:
            del data[key]

    # Write the modified data back to the JSON file
    with open(output, 'w') as f:
        json.dump(data, f, indent=4)


remove_keys_with_few_instances(json_file, json_file)


def combine_aliased_keys(json_file, output, alias_map):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    for key in alias_map:
        # Check if the key is an alias
        real_key = alias_map.get(key)
        # If the real key is not in combined_data, add it with the value
        json_data[real_key] += json_data[key]
        del json_data[key]
    with open(output, 'w') as f:
        json.dump(json_data, f, indent=4)


combine_aliased_keys('data/tweets/raw.json',
                     'data/tweets/clean.json', duplicates)
