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
    "FOX News Radio",
    "Fox News",
    "Fox Business",
    "FEMA",
    "Democratic Women's Caucus",
    "Face The Nation",
    "Heritage Foundation",
    "The White House 45 Archived",
    "House Committee on Natural Resources",
    "NBC News",
    "Morning Joe",
    "HHS.gov",
    "Travel - State Dept",
    "House Rules Committee",
    "RSC",
    "NASA",
    "IRSnews",
    "U.S. Army",
    "Select Committee on the Chinese Communist Party",
    "Committee on Transportation and Infrastructure",
    "Alliance for Retired Americans",
    "Washington Journal",
    "U.S. House Committee on Financial Services",
    "Breitbart News",
    "Ripon Advance",
    "FL Division of Emergency Management",
    "House Armed Services Democrats",
    "Pro-Choice Caucus",
    "Elon Musk",
    "RSBN",
    "Donald Trump Jr.",
    "LCV \u2013 League of Conservation Voters",
    "House Committee on Veterans' Affairs",
    "T&I Committee Republicans",
    "Social Security Works",
    "CSPAN",
    "Committee on Education & the Workforce Democrats",
    "January 6th Committee",
    "Committee on House Admn. Democrats",
    "House Homeland Security Committee Democrats",
    "Oversight Committee Democrats",
    "GOP",
    "State of the Union",
    "This Week",
    "House Veterans' Affairs Democrats",
    "Regional Leadership Council",
    "ALZ Impact Movement",
    "Acyn",
    "Aaron Rupar",
    "SBA",
    "House Homeland GOP",
    "House Committee on Education & the Workforce",
    "House Science Committee",
    "Family Research Council",
    "House GOP Policy",
    "Washington Examiner",
    "Wall Street Journal Opinion",
    "SBA Pro-Life America",
    "No Labels",
    "Senate Democrats",
    "ABC News Live",
    "House Agriculture Committee Democrats",
    "House Committee on Small Business",
    "RNC Research",
    "Heritage Action",
    "America First Legal",
    "The Iowa Torch",
    "Axios",
    "House Budget Committee Democrats",
    "msema",
    "The Epoch Times",
    "Biden-Harris HQ",
    "House Foreign Affairs Committee Dems",
    "U.S. Senate Banking Committee GOP",
    "NC Emergency Management",
    "Adam Kredo",
    "CBS News",
    "Senate VA Republicans",
    "SASC GOP",
    "House Appropriations Democrats",
    "FRCAction",
    "NWS Tallahassee",
    "Jake Tapper",
    "MLive",
    "Ohio Business Roundtable",
    "Black Maternal Health Caucus",
    "PA Democratic Party",
    "Rhode Island Foundation",
    "Institute for Gene Therapies",
    "National Debt Tweets",
    "Parliamentary Intelligence Security Forum",
    "The City Of New Orleans",
    "City of San Diego",
    "Congressional Equality Caucus",
    "AIPAC",
    "House Freedom Caucus",
    "Science Committee Democrats",
    "The New York Times",
    "Natural Resources Democrats",
    "FOX Business",
    "Congressional Hispanic Caucus",
    "Congressional Dads Caucus",
    "The Evening Edit",
]

duplicates = {
    "Rep. Ilhan Omar": "Ilhan Omar",
    "Vice President Kamala Harris": "Kamala Harris",
    "DeSantis War Room": "Ron DeSantis",
    "Congressman Greg Steube": "Greg Steube",
    "President Biden": "Joe Biden",
    "Former Rep. Tulsi Gabbard": "Tulsi Gabbard",
    "Team Perdue": "David Perdue",
    "Inhofe Press Office": "Sen. Jim Inhofe",
    "Congresswoman Ayanna Pressley": "Ayanna Pressley",
    "Attorney General Keith Ellison": "Keith Ellison",
    "Senator Mitt Romney": "Mitt Romney",
    "Rep. Josh Harder": "Josh Harder",
    "Rep. Dusty Johnson": "Dusty Johnson",
    "Office of Rep. Amash Archive": "Justin Amash",
}

# marie newman
# leader mcconnell
# rep nadler

# also weird symboled individuals


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
