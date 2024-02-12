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
