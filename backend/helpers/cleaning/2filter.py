import json
import re


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
    "Senate Judiciary Committee",
    "New York Post",
    "A Starting Point",
    "Veterans Affairs",
    "NWSHonolulu",
    "Problem Solvers Caucus",
    "US Department of the Interior",
    "Steak for Breakfast",
    "National Review",
    "Senate Foreign Relations Committee",
    "Senate Budget GOP",
    "UAW",
    "Weaponization Committee",
    "1819 News",
    "Neil Cavuto",
    "Stephen Miller",
    "Bill Melugin",
    "Jake Sherman",
    "Maria Bartiromo",
    "Matthew Foldi",
    "Ali Bradley",
    "Daily Caller",
    "The Democrats",
    "Rachel Campos-Duffy",
    "Henry Rodgers"
]

duplicates = {
    "Rep. Ilhan Omar": "Ilhan Omar",
    "Vice President Kamala Harris": "Kamala Harris",
    "DeSantis War Room": "Ron DeSantis",
    "Congressman Greg Steube": "Greg Steube",
    "President Biden": "Joe Biden",
    "Former Rep. Tulsi Gabbard": "Tulsi Gabbard",
    # "Team Perdue": "David Perdue",
    "Inhofe Press Office": "Sen. Jim Inhofe",
    "Congresswoman Ayanna Pressley": "Ayanna Pressley",
    "Attorney General Keith Ellison": "Keith Ellison",
    "Senator Mitt Romney": "Mitt Romney",
    "Rep. Josh Harder": "Josh Harder",
    "Rep. Dusty Johnson": "Dusty Johnson",
    "Office of Rep. Amash Archive": "Justin Amash",
    "Rep. Dean Phillips": "Dean Phillips",
    "Congresswoman Rashida Tlaib": "Rashida Tlaib",
    "Lieutenant Governor Antonio Delgado": "Antonio Delgado",
    "Congressman David N. Cicilline": "David Cicilline",
    "Lizzie Pannill Fletcher": "Lizzie Fletcher",
}

rename_map = {
    "CathyMcMorrisRodgers": "Cathy McMorris Rodgers",
    "Vice President Mike Pence Archived": "Mike Pence",
    "Archive: Rep. Cheri Bustos": "Cheri Bustos",
    "Archive: Rep. Jeb Hensarling": "Jeb Hensarling",
    "Archive: Rep. John Delaney": "John Delaney",
    "Former Rep. Daniel Lipinski": "Daniel Lipinski",
    "Col. Paul Cook (Ret.)": "Paul Cook",
    "Eleanor #DCStatehood Holmes Norton": "Eleanor Holmes Norton",
    "Archive: Rep. Ron Kind": "Ron Kind",
    "Archive: Steve Stivers": "Steve Stivers",
    "Archive: Sen. Heidi Heitkamp": "Heidi Heitkamp",
    "Pat Toomey (US Sen. ret.)": "Pat Toomey",
    "Archive: Senator Joe Donnelly": "Joe Donnelly",
    "Fmr. US Rep. Rick Nolan": "Rick Nolan",
    "Archive: Dave Loebsack (Retired US Rep)": "Dave Loebsack",
    "Senator Cortez Masto": "Catherine Cortez Masto",
    "Archived: U.S. Rep Kathleen Rice": "Kathleen Rice",
    "Archive: Congressman Tim Ryan": "Tim Ryan",
    "Archive: Nita Lowey": "Nita Lowey",
    "Rep. Gallagher Press Office": "Mike Gallagher",
    "Archive: Rep. John Shimkus": "John Shimkus",
    "Archived: Rep. Tom O'Halleran": "Tom O'Halleran",
    "Mark Sanford (Archived)": "Mark Sanford",
    "Office of Rep. Nicole Malliotakis": "Nicole Malliotakis",
    "Archive: Tom MacArthur": "Tom MacArthur",
    "Jared Golden for Congress": "Jared Golden",
    "Archived: Rep. Tom Malinowski": "Tom Malinowski",
    "Ben McAdams UT": "Ben McAdams",
    "Archived: Rep. Max Rose": "Max Rose",
    "Archived: Rep. Xochitl Torres Small": "Xochitl Torres Small",
    "CEO, Former Congresswoman, Author, Entrepreneur": "Marie Newman",
    "Archive: Senator Tom Udall": "Tom Udall",
    "Leader McConnell": "Mitch McConnell",
    "Rep. Nadler": "Jerry Nadler",
    "Rep. Cammack Press Office": "Kat Cammack",
    "Rep. Chip Roy Press Office": "Chip Roy",
    "Mac Thornberry Press": "Mac Thornberry",
    "Archive: U.S. Rep. Stephanie Murphy": "Stephanie Murphy",
    "MichelleLujanGrisham": "Michelle Lujan Grisham",
    "Donald M. Payne, Jr.": "Donald Payne Jr.",
    "Bill Pascrell, Jr.": "Bill Pascrell Jr.",
    "Congressmember Bass": "Karen Bass",
    "John Joyce, M.D.": "John Joyce",
    "Lacy Clay MO1st": "Lacy Clay",
}

titles = [
    "US Rep. ",
    "U.S. ",
    "Former ",
    "Fmr. ",
    "Rep.",
    "Sen.",
    "Sen ",
    "Rep ",
    "Hon. ",
    "Senator ",
    "Speaker",
    "Congressman",
    "Congresswoman",
    "Representative",
    "Dr.",
    "Secretary",
    "Governor",
    ", M.D.",
    "Cong. ",
    ", MD",
    ", Ph.D.",
    ", Jr.",
    "Del. ",
]


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


remove_keys_with_few_instances(json_file, json_file, min_instances=20)


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


def rename_keys(input, output, key_map, titles):
    """
    Rename keys in a dictionary according to a mapping provided.

    Parameters:
        d (dict): The dictionary to be modified.
        key_map (dict): A dictionary where keys are the current keys in `d`
                        and values are the new keys.

    Returns:
        dict: A new dictionary with keys renamed according to `key_map`.
    """
    with open(input, 'r') as f:
        d = json.load(f)
    data = {key_map.get(k, k): v for k, v in d.items()}
    for title in titles:
        # print(title)
        data = {k.replace(title, "").lstrip(): v for k, v in data.items()}

    with open(output, 'w') as f:
        json.dump(data, f, indent=4)


rename_keys('data/tweets/clean.json',
            'data/tweets/clean.json', rename_map, titles)
