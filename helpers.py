import hashlib
from pymongo import MongoClient
from urllib.parse import quote_plus
import json

import streamlit as st
import yaml
import re
from linkml.generators import shaclgen, owlgen
from linkml_runtime.dumpers import json_dumper
from linkml.validator import validate
from io import BytesIO
import zipfile
from urllib.parse import urljoin, quote_plus

import pymongo
import io
import glob


def clean_text(text):
    # Remove all punctuation except commas
    text = re.sub(r'[^\w\s,]', '', text)

    # Replace any whitespace (of any size) with one underscore
    text = re.sub(r'\s+', '', text)

    return text.split(',')


def generate_valid_url(base_url, path):
    # Trim leading and trailing spaces
    base_url = base_url.strip()
    path = path.strip()

    # Encode path to ensure it's safe for URL usage
    encoded_path = quote_plus(path)

    # Combine the base URL and the encoded path
    full_url = urljoin(base_url, encoded_path)

    return full_url


def contains_number(s):
    pattern = r"^-?\d+(\.\d+)?$"
    if s == '':
        return True
    else:
        return bool(re.search(pattern, s))


def pattern_test(s, regex):
    if re.fullmatch(regex, s):
        return True
    else:
        return False


def convert_to_number(s):
    # Regex for matching integers and floating-point numbers
    int_pattern = r"^-?\d+$"
    float_pattern = r"^-?\d+\.\d+$"

    # Check if the string is an integer
    if re.match(int_pattern, s):
        return int(s), 'int'
    # Check if the string is a float
    elif re.match(float_pattern, s):
        return float(s), 'float'
    else:
        raise ValueError(
            "The string does not represent a valid integer or floating-point number.")


def generate_said(data):
    data_string = str(data).encode()
    hash_object = hashlib.sha256()
    hash_object.update(data_string)
    return hash_object.hexdigest()


# Load Data into MongoDB
username = "admin"
password = "admin"
uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@localhost:27017/mydatabase?authSource=admin"
client = MongoClient(uri)
db = client['SemanticDataLink']
collection = db['SemanticDataLink']


def insert_capture_base(data, capture_base_hash):
    # Insert Data into MongoDBs
    # Check if a document with the same capture_base exists
    try:
        existing_document = collection.find_one(
            {"ref_capture_base": capture_base_hash})
        if existing_document is None:
            # If no existing document, insert the new data
            data['ref_capture_base'] = capture_base_hash
            # print(data)
            collection.insert_one(data)
            print("capture_base inserted.")
            return 0
        else:
            print("capture_base already exists.")
            return 1
    except:
        return -1


def insert_overlay(data, overlay_hash):
    # Insert Data into MongoDBs
    # Check if a document with the same capture_base exists
    try:
        existing_document = collection.find_one(
            {"overlay_hash": overlay_hash})
        if existing_document is None:
            # If no existing document, insert the new data
            data['overlay_hash'] = overlay_hash
            collection.insert_one(data)
            return 0
        else:
            return 1
    except:
        return -1


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


def count_keys_except(dictionary, key1='capture_base', key2='type', key3='language'):
    return sum(1 for key in dictionary if key not in [key1, key2, key3])

# Function to add a new enum type


def add_enum():

    enum_name = st.session_state.new_enum_name.strip()
    if enum_name and enum_name not in st.session_state.enums:
        st.session_state.enums[enum_name] = []
    else:
        st.error("Enum name is required and must be unique.")

# Function to remove an enum type


def remove_enum(enum_name):
    if enum_name in st.session_state.enums:
        del st.session_state.enums[enum_name]

# Function to add a value to an enum type


def add_enum_value(enum_name, value):
    if value and value not in st.session_state.enums[enum_name]:
        st.session_state.enums[enum_name].append(value.strip())
    else:
        st.error("Enum value is required and must be unique within the enum.")

# Function to remove a value from an enum type


def remove_enum_value(enum_name, value):
    st.session_state.enums[enum_name].remove(value)


def validate_linkml(main_prefix, dataset_id, dataset_name, attributes, prefixes):

    report = {}
    VALID = True

    if main_prefix == '':
        report['main_identifier'] = ':red[General Information -- Main Identifier] field is mandatory. Please choose a suitable Identifier for the Entity'
        VALID = False
    if dataset_id == '':
        report['dataset_id'] = ':red[General Information -- ID] field is mandatory. Please choose a suitable ID for the Entity'
        VALID = False
    if dataset_name == '':
        report['dataset_name'] = ':red[General Information -- Name] field is mandatory. Please choose a suitable name for the Entity'
        VALID = False

    # Attributes
    for attribute in attributes:
        if attribute['name'] == '':
            report['attribute_name'] = f':red[{attribute["name"]} - Name] field is mandatory. Please choose a suitable Name for the attribute'
            VALID = False
        if attribute['range'] == 'enum':
            if len(attribute['enums']) < 1:
                report['attribute_name'] = f':red[{attribute["range"]} - Enum] You select "Enum" datatype - please provide at least one possible enum.'
                VALID = False
        if attribute['range'] == "integer" or attribute['range'] == "float" or attribute['range'] == "decimal" or attribute['range'] == "double":
            if not contains_number(attribute['minimum_value']) or not contains_number(attribute['maximum_value']):
                report['attribute_min_max'] = f':red[{attribute["datatype"]} - Min und Max Values] Please provide valid min and / or max values for attribute]'
                VALID = False

    return VALID, report


def parse_linkml(main_prefix, dataset_id, dataset_name, attributes, prefixes):

    # Parse to LinkML Schema
    data_to_export = {
        # st.session_state.dataset_id,
        "id": generate_valid_url(main_prefix, dataset_id),
        "name": dataset_name,
        "prefixes": prefixes,
        "imports": "linkml:types",
        "default_range": "string",
        "classes": {
            dataset_id: {'attributes': {}}
        },
        "enums": {}
    }

    if len(attributes) >= 1:
        for details in attributes:
            if details['range'] != 'enum':
                data_to_export['classes'][dataset_id]['attributes'][details['name']] = {
                    key: value for key, value in details.items() if key not in ['name', 'pattern_check', 'enum']
                }
            if details['range'] == 'enum':
                data_to_export['enums'][list(details['enums'].keys())[0]] = {
                    "permissible_values": {k: v for k, v in details['enums'].items()}
                }

    linkml_schema = yaml.dump(
        data_to_export, sort_keys=False, allow_unicode=True)

    return linkml_schema


# [
#   {
#     "name": "asaasa",
#     "multivalued": true,
#     "required": true,
#     "pattern": true,
#     "datatype": "enum",
#     "slot_uri": "linkml:aasasasa",
#     "pattern_regex": "ssd",
#     "enums": {
#       "a": {
#         "description": "a",
#         "meaning": "a"
#       }
#     },
#     "description": "asasasas"
#   },
#   {
#     "name": "aasas",
#     "multivalued": false,
#     "required": true,
#     "pattern": false,
#     "datatype": "integer",
#     "slot_uri": "",
#     "pattern_regex": "",
#     "minimum_value": "0",
#     "maximum_value": "5",
#     "description": "asasasas"
#   }
# ]
