import re
import json


def normalize_name(name):
    pattern = re.compile(
        r'^(Rep\.|Senator|Speaker|Archive:)\s+', re.IGNORECASE)

    while True:
        new_name = pattern.sub('', name)
        if new_name == name:
            break
        name = new_name

    name = re.sub(r'\b[A-Z]\.\s*', '', name)
    name = re.sub(r'\s+(Jr\.|Sr\.)', '', name)

    return name.strip()


def flip_name(name):
    name = name.split()
    return name[-1] + " " + " ".join(name[:-1])


def update_json(input_json, people_csv):
    people_data = json.loads(people_csv)
    people_dict = {normalize_name(
        person['name']): person for person in people_data}

    for _, match in enumerate(input_json['matches']):
        normalized_match = normalize_name(match)
        # print(normalized_match)
        # print(flip_name(normalized_match))
        if normalized_match in people_dict:
            person = people_dict[normalized_match]
            input_json['country'] = input_json.get(
                'country', []) + [person['country']]
            input_json['chamber'] = input_json.get(
                'chamber', []) + [person['chamber']]
            input_json['party'] = input_json.get(
                'party', []) + [person['party']]
            input_json['region'] = input_json.get(
                'region', []) + [person['region']]
        elif flip_name(normalized_match) in people_dict:
            person = people_dict[flip_name(normalized_match)]
            input_json['country'] = input_json.get(
                'country', []) + [person['country']]
            input_json['chamber'] = input_json.get(
                'chamber', []) + [person['chamber']]
            input_json['party'] = input_json.get(
                'party', []) + [person['party']]
            input_json['region'] = input_json.get(
                'region', []) + [person['region']]
        else:
            input_json['country'] = input_json.get(
                'country', []) + ["Not Found"]
            input_json['chamber'] = input_json.get(
                'chamber', []) + ["Not Found"]
            input_json['party'] = input_json.get('party', []) + ["Not Found"]
            input_json['region'] = input_json.get('region', []) + ["Not Found"]

    return input_json
