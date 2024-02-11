import streamlit as st
import yaml
import re
from linkml.generators import shaclgen, owlgen
from io import BytesIO
import zipfile

st.set_page_config(layout="wide")


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


# Predefined datatypes for selection
predefined_datatypes = ["string", "integer", "float", "boolean", "date", "enum", "datetime", "decimal", "double",
                        "HttpsIdentifier", "uri"]

# Initialize session state for dynamic global variables and predefined datatypes
if 'global_vars' not in st.session_state:
    st.session_state.global_vars = {"linkml": "https://w3id.org/linkml/"}
if 'datatype_selections' not in st.session_state:
    st.session_state.datatype_selections = predefined_datatypes
if 'num_attributes' not in st.session_state:
    st.session_state.num_attributes = 0
if 'attribute_details' not in st.session_state:
    st.session_state.attribute_details = {}

if 'dataset_id' not in st.session_state:
    st.session_state.dataset_id = {}
if 'dataset_name' not in st.session_state:
    st.session_state.dataset_name = {}
if 'class_uri' not in st.session_state:
    st.session_state.class_uri = {}

# Sidebar for general information, global variables, and attribute manipulation
with st.sidebar:

    st.subheader("General Information")
    st.session_state.dataset_id = st.text_input(
        "ID", placeholder="https://yourschema.org/")
    st.session_state.dataset_name = st.text_input(
        "Name", placeholder="yourSchemaName")

    st.divider()

    st.subheader("Prefixes")
    for key, value in st.session_state.global_vars.items():
        st.text(f"{key}: {value}")

    global_var_key = st.text_input("Add Prefix (Key)", placeholder="linkml")
    global_var_value = st.text_input(
        "Add Prefix (Value)", placeholder="https://w3id.org/linkml/")
    if st.button('Add Prefix'):
        if global_var_key and global_var_value:
            st.session_state.global_vars[global_var_key] = global_var_value
            st.rerun()
            # Update without rerun to maintain selections

    # Delete global variable
    deletable_keys = list(st.session_state.global_vars.keys())
    deletable_keys.remove('linkml')
    delete_var_key = st.selectbox(
        "Delete Global Variable", [''] + deletable_keys)
    if st.button('Delete Selected Prefix'):
        if delete_var_key and delete_var_key in st.session_state.global_vars:
            del st.session_state.global_vars[delete_var_key]

    st.divider()

    st.subheader("Attributes")
    if st.button('Add Attribute', type='primary'):
        st.session_state.num_attributes += 1

    # Button to delete the last added attribute
    if st.button('Delete Last Attribute') and st.session_state.num_attributes > 0:
        # Remove the last attribute's details from the session state
        del st.session_state.attribute_details[st.session_state.num_attributes]
        st.session_state.num_attributes -= 1

# Function to add a single attribute section


def add_attribute(idx, global_vars, datatype_selections):
    enum_values = ''
    minimum_value = 0
    maximum_value = 0
    pattern_regex = ''
    slot_uri_value = ''
    description = ''
    # Retrieve existing details if any
    details = st.session_state.attribute_details.get(idx, {})
    with st.container():
        # Name attribute
        st.markdown(f'**Attribute {idx}**')

        col1, col2 = st.columns([4, 1])
        col3, col4 = st.columns([3, 1])
        col5, col6 = st.columns([3, 1])
        col7, col8 = st.columns([2, 2])
        col9, col10 = st.columns([1, 3])

        with col1:
            name = st.text_input(f":red[Name]*", value=details.get(
                'name', ''), key=f"name_{idx}")
            if name == "":
                st.error(f':red[Name] can not be empty')
            else:
                st.success(f'Input saved --- (  {name}  )')
        with col2:
            multivalued = st.checkbox(f"Multivalued", value=details.get(
                'multivalued', ''), key=f"multivalued_{idx}")
            required = st.checkbox(f"Required", value=details.get(
                'required', ''), key=f"required_{idx}")
            pattern = st.checkbox(f"Pattern", value=details.get(
                'pattern', ''), key=f"pattern_{idx}")

        with col3:
            datatype = st.selectbox(f":red[Datatype]*", datatype_selections, index=datatype_selections.index(details.get(
                'datatype', 'int')) if details.get('datatype', 'int') in datatype_selections else 0, key=f"datatype_{idx}")
            if datatype == 'enum':
                with col4:
                    enum_values = st.text_input(
                        f"Enum Values {idx} (comma-separated)", value=details.get('enum_values', ''), key=f"enum_values_{idx}")

                    if len(list(enum_values.split(','))) < 1:
                        st.error("Please provide at least one option")

                    st.write(list(enum_values.split(',')))
                    # if enum_values != '':
                    #     enum_values_list = list(enum_values.split(','))
                    # else:
                    #     enum_values_list = ''
            if datatype == "integer" or datatype == "float" or datatype == "decimal" or datatype == "double":
                with col4:
                    minimum_value = st.text_input(
                        "Minimum Value:", key=f"minimum_number_{idx}")
                    if contains_number(minimum_value) == False:
                        st.error('Please enter a valid number')
                    maximum_value = st.text_input(
                        "Maximum Value:", key=f"maximum_number_{idx}")
                    if contains_number(maximum_value) == False:
                        st.error('Please enter a valid number')

        with col5:
            global_var_selection = st.selectbox(
                f"Slot_URI", ['None'] + list(global_vars.keys()), key=f"prefix_selection_{idx}")
            if global_var_selection != 'None':
                with col6:
                    slot_uri_value = st.text_input(
                        f"Value:", placeholder='<class / attribute>', key=f"slot_uri_{idx}")
            if global_var_selection != 'None' and slot_uri_value != "":
                st.write(f"{global_var_selection} : {slot_uri_value}")

            details['global_var'] = global_var_selection if global_var_selection != 'None' else ''

        if pattern:
            with col7:
                pattern_regex = st.text_input(
                    "Pattern for Data Validation [regex]:", key=f"pattern_regex_{idx}")
            with col8:
                pattern_regex_test = st.text_input(
                    "Pattern Test:", key=f"pattern_regex_test_{idx}")
                if pattern_regex_test != '':
                    if pattern_test(pattern_regex_test, pattern_regex):
                        st.success('Valid Input String')
                    else:
                        st.error('String does not match pattern')

        # Description
        with col9:
            description_checkbox = st.checkbox(
                f"Add Description", key=f"description_checkbox_{idx}", value=details.get(
                    'description_checkbox', ''))
        if description_checkbox:
            with col10:
                description = st.text_input(
                    "Attribute description (free text):", key=f"description_{idx}", value=details.get(
                        'description', ''))

    # Update the session state with the latest details
    st.session_state.attribute_details[idx] = {
        "name": name,
        "datatype": datatype,
        "enum_values": enum_values,
        "minimum_value": minimum_value,
        "maximum_value": maximum_value,
        "multivalued": multivalued,
        "required": required,
        "pattern": pattern,
        "pattern_regex": pattern_regex,
        "slot_uri": f"{global_var_selection}:{slot_uri_value}",
        "description_checkbox": description_checkbox,
        "description": description
    }  # "enum_values": details['enum_values']


# Main section for attributes and export button
st.title("Define Attributes")
for i in range(1, st.session_state.num_attributes + 1):
    add_attribute(i, st.session_state.global_vars,
                  st.session_state.datatype_selections)

st.text("")
st.divider()

# Export and Validate
if st.button('Export and Validate LinkML', type='primary'):

    attributes_yaml = {}
    all_good = True

    if st.session_state.dataset_id == '':
        st.error(
            f':red[General Information -- ID] field is mandatory. Please choose a suitable ID for the Entity')
        all_good = False

    if st.session_state.dataset_name == '':
        st.error(
            f':red[General Information -- Name] field is mandatory. Please choose a suitable name for the Entity')
        all_good = False

    # Attributes
    for idx, details in st.session_state.attribute_details.items():

        if details['name'] == '':
            st.error(
                f':red[Name] field is mandatory. Please choose a suitable Name for the attribute')
            all_good = False
        if details['datatype'] == 'enum':
            if len(details['enum_values']) < 1:
                st.error(
                    f':red[Enum] You select "Enum" datatype - please provide at least one possible enum.')
                all_good = False
        if details['datatype'] == "integer" or details['datatype'] == "float" or details['datatype'] == "decimal" or details['datatype'] == "double":
            if details['minimum_value'] and details['maximum_value'] == 0:
                st.error(
                    f':red[Min und Max Values] Please select different min and max values for attribute :red[{idx}]')
                all_good = False

    if all_good:
        # Add default prefix
        st.session_state.global_vars[
            st.session_state.dataset_id] = f'https://schema.org/{st.session_state.dataset_id}'

        data_to_export = {
            # st.session_state.dataset_id,
            "id": f'https://schema.org/{st.session_state.dataset_id}',
            "name": st.session_state.dataset_name,
            "prefixes": st.session_state.global_vars,
            "imports": "linkml:types",
            "default_range": "string",
            "classes": {
                st.session_state.dataset_id: {'attributes': {}}
            },
            "enums": {}
        }

        for idx, details in st.session_state.attribute_details.items():
            data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']] = {
            }
            if details['datatype'] == 'enum':
                data_to_export['enums'][details['name']] = {
                    "permissible_values": {k: {'description': ''} for k in details["enum_values"]}}
            elif details['datatype'] == "integer" or details['datatype'] == "float" or details['datatype'] == "decimal" or details['datatype'] == "double":
                data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                     ]['range'] = details['datatype']
                data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                     ]['minimum_value'] = float(details['minimum_value'])
                data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                     ]['maximum_value'] = float(details['maximum_value'])
            else:
                data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                     ]['range'] = details['datatype']

            data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                 ]['required'] = details['required']
            data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                 ]['multivalued'] = details['multivalued']

            if details['pattern']:
                data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                     ]['pattern'] = details['pattern_regex']

            if details['slot_uri'] != 'None:':
                data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                     ]['slot_uri'] = details['slot_uri']

            if details['description_checkbox']:
                data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                     ]['description'] = details['description']

        yaml_str = yaml.dump(
            data_to_export, sort_keys=False, allow_unicode=True)
        st.text_area("YAML Output", yaml_str, height=300)

        rdf_test_successfull = False
        try:
            # Attempt to generate the SHACL graph
            shacl_out = shaclgen.ShaclGenerator(str(yaml_str)).as_graph()
            st.success("SHACL graph generation successful.")
            rdf_test_successfull = True
        except Exception as e:
            # Handle exceptions specific to ShaclGenerator
            st.error(f"An error occurred during SHACL generation: {e}")
            rdf_test_successfull = False

        try:
            # Attempt to generate the OWL graph
            owl_out = owlgen.OwlSchemaGenerator(str(yaml_str)).as_graph()
            st.success("OWL graph generation successful.")
            rdf_test_successfull = True
        except Exception as e:
            # Handle exceptions specific to OwlSchemaGenerator
            st.error(f"An error occurred during OWL generation: {e}")
            rdf_test_successfull = False

        if rdf_test_successfull:

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

            # # Function to serialize graphs to Turtle format
            # def serialize_graph_to_ttl(graph):
            #     return graph.serialize(format='turtle')

            # # Serialize SHACL graph to Turtle
            # shacl_ttl = serialize_graph_to_ttl(shacl_out)
            # st.download_button(label="Download SHACL Graph",
            #                    data=shacl_ttl,
            #                    file_name="shacl_graph.shacl.ttl",
            #                    mime='text/turtle')

            # # Button to download OWL graph
            # # Serialize OWL graph to Turtle
            # owl_ttl = serialize_graph_to_ttl(owl_out)
            # st.download_button(label="Download OWL Graph",
            #                    data=owl_ttl,
            #                    file_name="owl_graph.ttl",
            #                    mime='text/turtle')


# if st.button('Export to YAML', type='primary'):
#     # General attributes missing
#     st.json(st.session_state.attribute_details)
#     attributes_yaml = []
#     for idx, details in st.session_state.attribute_details.items():
#         attribute_yaml = {
#             "name": details['name'],
#             "type": details['datatype'],
#             "multivalued": details['multivalued'],
#             # "global_var": details['global_var']
#         }
#         if details['datatype'] == 'enum':
#             attribute_yaml['permissible_values'] = {
#                 value: {} for value in details['enum_values']}
#         attributes_yaml.append(attribute_yaml)

#     data_to_export = {
#         "dataset_id": dataset_id,
#         "dataset_name": dataset_name,
#         "global_vars": st.session_state.global_vars,
#         "attributes": attributes_yaml
#     }
#     yaml_str = yaml.dump(data_to_export, sort_keys=False, allow_unicode=True)
#     st.text_area("YAML Output", yaml_str, height=300)
