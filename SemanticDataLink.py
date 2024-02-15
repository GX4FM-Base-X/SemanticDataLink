import streamlit as st
import yaml
from helpers import *

st.set_page_config(layout="wide")
st.title('Semantic Data Link')

# Attributes
if 'attributes' not in st.session_state:
    st.session_state.attributes = []
if 'PREFIXES' not in st.session_state:
    st.session_state.PREFIXES = {"linkml": "https://w3id.org/linkml/"}
if 'ENUMS' not in st.session_state:
    st.session_state.ENUMS = {}
if 'SELECT' not in st.session_state:
    st.session_state.SELECT = []

# Function to add a new attribute


def add_attribute():
    st.session_state.attributes.append({})


def delete_attribute():
    to_delete = len(st.session_state.attributes) - 1
    del st.session_state.attributes[to_delete]


# Basic info
st.subheader("Basic Information")
main_prefix = st.text_input(
    "Main Identifier", value="https://base-x-ecosystem.com/")
id = st.text_input("ID", value="base-x-core")
if id == '':
    st.error(
        f':red[Basic Information -- ID] field is mandatory. Please choose a suitable ID for the Entity')
linkml_id = generate_valid_url(main_prefix, id)
st.write(f"LinkML ID *(Main Identifier + ID)*: {linkml_id}")
name = st.text_input("Name")
if name == '':
    st.error(
        f':red[Basic Information -- Name] field is mandatory. Please choose a suitable name for the Entity')

# Prefixes

st.subheader("Prefixes")
for key, value in st.session_state.PREFIXES.items():
    st.text(f"{key}: {value}")

# Add Prefix
prefix_key = st.text_input("Add Prefix (Key)", placeholder="linkml")
prefix_value = st.text_input(
    "Add Prefix (Value)", placeholder="https://w3id.org/linkml/")
if st.button('Add Prefix', type='primary'):
    if prefix_key and prefix_value:
        st.session_state.PREFIXES[prefix_key] = prefix_value
        st.rerun()
# Delete Prefix
col1, _, _, _, _ = st.columns(5)
with col1:
    deletable_keys = list(st.session_state.PREFIXES.keys())
    deletable_keys.remove('linkml')
    delete_var_key = st.selectbox(
        "Delete Global Variable", [''] + deletable_keys)

    if st.button('Delete Selected Prefix'):
        if delete_var_key and delete_var_key in st.session_state.PREFIXES:
            del st.session_state.PREFIXES[delete_var_key]
            st.rerun()

st.divider()

# Attribute customization
st.subheader("Attributes")
col1, col2 = st.columns(2)
with col1:
    # st.button('Add Attribute', on_click=add_attribute, type='primary')
    # UI to add a new attribute
    if st.button('Add Attribute', key='attribute_add', type='primary'):
        add_attribute()
with col2:
    # st.button('Delete last Attribute', on_click=delete_attribute)
    if st.button('Delete Last Attribute', key='attribute_delete'):
        delete_attribute()

# attributes = {}
# for idx in range(st.session_state.ATTRIBUTES):
for idx, attribute in enumerate(st.session_state.attributes):
    # Get all Prefixes
    prefixes = list(st.session_state.PREFIXES.keys())

    # Add attribute
    attribute_name = st.text_input(
        "Attribute Name", key=f'attribute_name_{idx}')
    if attribute_name == '':
        st.error('Attribute Name can not be empty!')
        break

    attribute[attribute_name] = {}

    attribute[attribute_name]['multivalued'] = st.checkbox(
        "Multivalued", value=False, key=f'attribute_multivalued_{idx}')
    attribute[attribute_name]['identifier'] = st.checkbox(
        "Identifier", value=False, key=f'attribute_identifier_{idx}')
    attribute[attribute_name]['required'] = st.checkbox("Required", value=False,
                                                        key=f'attribute_required_{idx}')
    enum_name = f"{attribute_name.upper()}_ENUM"
    attribute[attribute_name]['range'] = st.selectbox("Datatype", ["string", "integer", "float", "boolean",
                                                                   "date", enum_name, "datetime", "decimal", "double", "HttpsIdentifier", "uri"], key=f'attribute_datatype_{idx}')
    # Enums customization (simplified for this example)
    if attribute[attribute_name]['range'] == enum_name:
        enum_values = st.text_input(
            "Enum Values (comma-separated, all punctuation except comma is removed)", value="", key=f'attribute_enums_{idx}')
        if enum_values != '':
            try:
                cleaned_enums = clean_text(enum_values)

                # Enter More Information about enums
                if len(cleaned_enums) == 0:
                    break
                st.session_state.ENUMS[enum_name] = {
                    "permissible_values": {}
                }
                for idxx, e in enumerate(cleaned_enums):

                    col1, col2 = st.columns([1, 3])
                    with col1:
                        enum_description_select = st.checkbox(
                            f"**{e}** - Add Description:", value=False, key=f'enum_description_select_{idx}_{idxx}')
                    with col2:
                        enum_description = ''
                        if enum_description_select:
                            enum_description = st.text_input(
                                "Description", key=f'enum_description_{idx}_{idxx}')
                            if enum_description == '':
                                st.error(
                                    f"You need to describe your enum")
                    col1, col2, col3 = st.columns([1, 2, 2])
                    with col1:
                        enum_meaning_select = st.checkbox(
                            f"**{e}** - Add Meaning:", value=False, key=f'enum_meaning_select_{idx}_{idxx}')
                        st.divider()
                    with col2:
                        enum_meaning_key = ''
                        if enum_meaning_select:
                            enum_meaning_key = st.selectbox(
                                "Meaning (Add Prefixes above if neccessary)", [''] + prefixes, key=f'enum_meaning_key_{idx}_{idxx}')
                            if enum_meaning_key == '':
                                st.error(
                                    f"You need to select a prefix")
                    with col3:
                        enum_meaning_class = ''
                        if enum_meaning_select:
                            enum_meaning_class = st.text_input(
                                "Enum Meaning Class", key=f'enum_meaning_class_{idx}_{idxx}')
                            if enum_meaning_class == '':
                                st.error(
                                    f"You need to add a class")
                    # Write enums to dict
                    if enum_description_select and enum_meaning_select:
                        # st.session_state.ENUMS[enum_name]["permissible_values"][e]
                        d_out = {
                            "description": enum_description,
                            "meaning": f"{enum_meaning_key}:{enum_meaning_class}"
                        }

                    if enum_description_select and enum_meaning_select == False:
                        # st.session_state.ENUMS[enum_name]["permissible_values"][e]
                        d_out = {
                            "description": enum_description
                        }
                    if enum_description_select == False and enum_meaning_select and enum_meaning_key != '' and enum_meaning_class != '':
                        # st.session_state.ENUMS[enum_name]["permissible_values"][e]
                        d_out = {
                            "meaning": f"{enum_meaning_key}:{enum_meaning_class}"
                        }

                    if enum_description_select == False and enum_meaning_select == False:
                        # st.session_state.ENUMS[enum_name]["permissible_values"][e]
                        # st.session_state.ENUMS.pop(enum_name, 'None')
                        d_out = {}

                    st.session_state.ENUMS[enum_name]["permissible_values"][e] = d_out

                    # Delete all remaining values
                    keep_list = list(set(
                        st.session_state.ENUMS[enum_name]["permissible_values"][e].keys()) - set(cleaned_enums))
                    for k in keep_list:
                        st.session_state.ENUMS[enum_name]["permissible_values"].pop(
                            k, 'None')
            except Exception as e:
                st.error(
                    f"Please enter valid enum values separated by commas: {e}")
        else:
            st.error('Please enter at least one value.')

    if attribute[attribute_name]['range'] == "integer" or attribute[attribute_name]['range'] == "float" or attribute[attribute_name]['range'] == "decimal" or attribute[attribute_name]['range'] == "double":
        col1, _, col2, _ = st.columns(4)
        with col1:
            minimum_value = st.text_input(
                "Minimum Value", value="", key=f'attribute_minimum_{idx}')
            if minimum_value != '':
                checker = contains_number(minimum_value)
                if checker:
                    attribute[attribute_name]['minimum_value'] = minimum_value
                if not checker:
                    st.error(
                        f"Please enter a valid number or leave blank")
        with col2:
            maximum_value = st.text_input(
                "Maximum Value", value="", key=f'attribute_maximum_{idx}')
            if maximum_value != '':
                checker = contains_number(maximum_value)
                if checker:
                    attribute[attribute_name]['maximum_value'] = maximum_value
                if not checker:
                    st.error(
                        f"Please enter a valid number or leave blank")
    # Slot URIs
    col1, col2 = st.columns(2)
    with col1:
        slot_uri_select = st.selectbox(
            "Slot URIs:", [''] + prefixes, key=f'attribute_slut_uri_selector_{idx}')
    with col2:
        slot_uri_class = st.text_input(
            "URI Class", key=f'attribute_slot_uri_class_{idx}')
        if slot_uri_select != '' and slot_uri_class == '':
            st.error(
                f"If you select a slot_uri you need to pass a target class")
    if slot_uri_select != '' and slot_uri_class != '':
        attribute[attribute_name]['slot_uri'] = f"{slot_uri_select}:{slot_uri_class}"
        st.write(f"Your slot_uri: **{slot_uri_select} : {slot_uri_class}**")
    # Description
    col1, col2 = st.columns([1, 3])
    with col1:
        description_check = st.checkbox(
            "Description", value=False, key=f'description_check_{idx}')
    if description_check:
        with col2:
            attribute[attribute_name]['description'] = st.text_input(
                "Description", key=f'attribute_description_select_{idx}')
    # REGEX Pattern
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        pattern_check = st.checkbox(
            "Pattern", value=False, key=f'attribute_pattern_{idx}')
    if pattern_check:
        with col2:
            attribute[attribute_name]['pattern'] = st.text_input(
                "REGEX Pattern", placeholder="^-?\d+$ (Match integer)", key='attribute_pattern_select')
        with col3:
            pattern_test_string = st.text_input(
                "Test Input for Pattern", key=f'attribute_pattern_test_string_{idx}')
            if attribute[attribute_name]['pattern'] != '' and pattern_test_string != '':
                if pattern_test(pattern_test_string, attribute['pattern']):
                    st.success('Valid Input String')
                else:
                    st.error('String does not match pattern')

    st.divider()
    st.divider()

# Attribute customization
if len(st.session_state.attributes) > 2:
    st.subheader("Attributes")
    col1, col2 = st.columns(2)
    with col1:
        # st.button('Add Attribute', on_click=add_attribute, type='primary')
        # UI to add a new attribute
        if st.button('Add Attribute', key='attribute_add_bottom', type='primary'):
            add_attribute()
    with col2:
        # st.button('Delete last Attribute', on_click=delete_attribute)
        if st.button('Delete Last Attribute', key='attribute_delete_bottom'):
            delete_attribute()

st.empty()
st.divider()
st.empty()

st.subheader('Semantic Data Link Overlays')
st.markdown('''
                Overlays are task-specific objects that provide cryptographically-bound layers 
                of definitional or contextual metadata to a Capture Base. 
                Any actor interacting with a published Capture Base can use Overlays 
                to transform how inputted data and metadata are displayed to a 
                viewer or guide an agent in applying a custom process to captured data.

                #### Important
                
                You can click on each expander to enter individual data. NOTE: The differnt overlays
                have general fields (*capture_base*, *type* and *language*) and fields which define the overlay.
                For example *size* in the *morphology_size* overlay. If you don't enter any value in the defining fields,
                than the overlay is not considered when generating the final JSON Output Document!
                Also do not forget to confirm your entry in each field (Mac: ⌘ + ↩).    
                ```
    ''')

with st.expander(label=':red[**Global Vs. Attribute specific**]'):
    st.markdown("""
        Many Overlays contain entities that is related to the whole overlay as well as entities that are dataset-attribute specific.
        Keep in mind that only the data [items specified for the python programming language are valid](https://www.geeksforgeeks.org/python-data-types/)! These are:
        ```json
        {
            "numeric": {
                "Integer": "int",
                "Float": "float", 
            }
            "dictionary": "dict",
            "boolean": "bool",
            "set": "set",
            "sequence_type": {
                "Strings": "str",
                "Lists": "list",
                "Tuple": "tuple"
            }
        }
        ```

        An example is the `semantic_unit.json` overlay:
        
        ```json
        {
            "capture_base":"f1b325f4edc10ea1dd41980b14de6d658e5b5befec01d01bebecfac2c69a81d6"
            "type":"spec/overlays/semantic/unit/1.0"
            "language":"en"
            "unit":""
            "attr_unit":{}
        }
        ```
        Here a global unit for the whole overlay can be specified (`unit`) or different units for the different atributes of the dataset can be set (`attr_unit`).
        Example Input:
        ```json
        {
            "capture_base":"f1b325f4edc10ea1dd41980b14de6d658e5b5befec01d01bebecfac2c69a81d6"
            "type":"spec/overlays/semantic/unit/1.0"
            "language":"en"
            "unit":"kg/s"
            "attr_unit":{
                "age": "int"
                "name": "str"
                "weight": "float"
            }
        }
    """)

# Sample JSON data for different options
# pragmatic, semantic, morphologic = allClasses()
files = glob.glob("oca/overlays/*.yaml")
# options = {
#     "Morphologic": [x for x in files if x.split('/')[-1].split('_')[0] == 'morphology'],
#     "Semantic": [x for x in files if x.split('/')[-1].split('_')[0] == 'semantic'],
#     "Pragmatic": [x for x in files if x.split('/')[-1].split('_')[0] == 'pragmatic']
# }
attributes = {}
for idx, f in enumerate(files):
    try:
        yaml_data = load_yaml(f)
        # st.write(yaml_data['attribute'][0])
        attributes[idx] = yaml_data['attribute'][0]
    except Exception as e:
        st.write(e)

st.divider()

options = []
for d in range(len(attributes.keys())):
    options.append(attributes[d]['name'].upper())

# Multiselect widget to choose options
overlay_inputs = []
# if len(options) > 0:
st.session_state.SELECT = st.multiselect(
    "Select Options", options, placeholder='Please select Overlays')
count = 0
# for option in options_multiselect:
for d in range(len(attributes.keys())):
    # Add top-level key to dict
    user_inputs = {}
    if attributes[d]['name'].upper() in st.session_state.SELECT:
        with st.expander(attributes[d]['name'].upper(), expanded=True):
            props = []
            for prop, value in attributes[d]['properties'].items():
                if prop == 'range':
                    user_input = st.selectbox(
                        f"{attributes[d]['name']} - Range",
                        ["string", "integer", "float", "boolean", "date", "enum",
                            "datetime", "decimal", "double", "HttpsIdentifier", "uri"],
                        index=["string", "integer", "float", "boolean", "date", "enum",
                               "datetime", "decimal", "double", "HttpsIdentifier", "uri"].index(value),
                        key=count
                    )
                    props.append((prop, user_input))
                elif prop in ['multivalued', 'identifier', 'required']:
                    user_input = st.checkbox(
                        f"{attributes[d]['name']} - {prop.capitalize()}", value, key=count)
                    props.append((prop, user_input))
                elif prop == 'pattern':
                    user_input = st.text_input(
                        f"{attributes[d]['name']} - Pattern", value, key=count)
                    props.append((prop, user_input))
                elif prop == 'slot_uri':
                    user_input = st.text_input(
                        f"{attributes[d]['name']} - Slot URI", value, key=count)
                    props.append((prop, user_input))

                count += 1

            st.divider()
            overlay_name = f"OVERLAY_{attributes[d]['name'].upper()}"
            user_inputs[overlay_name] = {
                x[0]: x[1] for x in props
            }
            overlay_inputs.append(user_inputs)

        st.divider()

# COMBINE ATTRIBUTES AND OVERLAYS
link_attributes_joined = st.session_state.attributes + overlay_inputs
linkml_attributes = dict(
    pair for d in link_attributes_joined for pair in d.items())


# Prepare the LinkML document structure
linkml_document = {
    "id": linkml_id,
    "name": name,
    "prefixes": {
        "linkml": "https://w3id.org/linkml/",
        id: linkml_id
    },
    "imports": "linkml:types",
    "default_prefix": id,
    "default_range": "string",
    "classes": {
        name: {
            "attributes": linkml_attributes
        }
    },
    "enums": st.session_state.ENUMS
}

st.empty()
st.divider()
st.empty()

on = st.toggle('Generate LinkML Schema')
if on:
    if name == '':
        st.error(
            f':red[Basic Information -- Name] field is mandatory. Please choose a suitable name for the Entity')
    else:
        # Serialize the document to YAML
        yaml_str = yaml.dump(
            linkml_document, sort_keys=False, allow_unicode=True)

        # # Display the YAML
        # st.subheader("LinkML Document in YAML Format")
        # st.text_area("YAML Output", yaml_str, height=300)

        try:
            # Attempt to generate the SHACL graph
            shacl_out = shaclgen.ShaclGenerator(
                str(yaml_str)).as_graph()
            st.success("SHACL graph generation successful.")
        except Exception as e:
            # Handle exceptions specific to ShaclGenerator
            st.error(f"An error occurred during SHACL generation: {e}")

        try:
            # Attempt to generate the OWL graph
            owl_out = owlgen.OwlSchemaGenerator(
                str(yaml_str)).as_graph()
            st.success("OWL graph generation successful.")
        except Exception as e:
            # Handle exceptions specific to OwlSchemaGenerator
            st.error(f"An error occurred during OWL generation: {e}")

        # Print LinkML YAML Schema
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_area(
                "YAML Output", yaml_str, height=300)
        with col2:
            st.text_area("OWL", owl_out.serialize(), height=300)
        with col3:
            st.text_area("SHACL", shacl_out.serialize(), height=300)

    # Function to serialize a graph and add it to a ZIP file
    def add_graph_to_zip(zipfile_obj, graph, filename):
        # Serialize the graph to Turtle format
        ttl_data = graph.serialize(format='turtle')
        zipfile_obj.writestr(filename, ttl_data)

    # Create a ZIP file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        add_graph_to_zip(zip_file, shacl_out, 'shacl_graph.ttl')
        add_graph_to_zip(zip_file, owl_out, 'owl_graph.ttl')

    # Prepare the ZIP file for downloading
    zip_buffer.seek(0)
    zip_bytes = zip_buffer.getvalue()

    st.download_button(label="Download Graphs (SHACL and OWL)",
                       data=zip_bytes,
                       file_name="graphs.zip",
                       mime="application/zip")
