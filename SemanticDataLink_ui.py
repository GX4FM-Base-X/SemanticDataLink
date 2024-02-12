from helpers import *

st.set_page_config(layout="wide")


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
if 'main_prefix' not in st.session_state:
    st.session_state.main_prefix = {}
if 'dataset_name' not in st.session_state:
    st.session_state.dataset_name = {}
if 'class_uri' not in st.session_state:
    st.session_state.class_uri = {}

if 'rdf_test_successfull' not in st.session_state:
    st.session_state.rdf_test_successfull = False
if 'said' not in st.session_state:
    st.session_state.said = {}
if 'yaml_string' not in st.session_state:
    st.session_state.yaml_string = {}

# Sidebar for general information, global variables, and attribute manipulation
with st.sidebar:

    st.subheader("General Information")
    st.session_state.main_prefix = st.text_input(
        "Main Prefix", value="https://base-x-ecosystem.com/")
    st.session_state.dataset_id = st.text_input(
        "ID", placeholder="base-schema")
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
            # st.rerun()
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
st.title("SemanticDataLink - Base Attributes")
for i in range(1, st.session_state.num_attributes + 1):
    add_attribute(i, st.session_state.global_vars,
                  st.session_state.datatype_selections)

st.text("")
st.divider()

# Export and Validate
if st.button('Validate LinkML', type='primary'):

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
            st.session_state.dataset_id] = st.session_state.main_prefix

        valid_url = generate_valid_url(
            st.session_state.main_prefix, st.session_state.dataset_id)
        data_to_export = {
            # st.session_state.dataset_id,
            "id": valid_url,
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
                # Validate Numbers
                minimum_value, minimum_value_type = convert_to_number(
                    details['minimum_value'])
                maximum_value, maximum_value_type = convert_to_number(
                    details['maximum_value'])
                if minimum_value_type == 'int':
                    data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                         ]['minimum_value'] = minimum_value
                if minimum_value_type == 'float':
                    data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                         ]['minimum_value'] = minimum_value
                if minimum_value_type != 'int' and minimum_value_type != 'float':
                    st.error('Please enter a valid minium number')

                if maximum_value_type == 'int':
                    data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                         ]['maximum_value'] = maximum_value
                if maximum_value_type == 'float':
                    data_to_export['classes'][st.session_state.dataset_id]['attributes'][details['name']
                                                                                         ]['maximum_value'] = maximum_value
                if maximum_value_type != 'int' and maximum_value_type != 'float':
                    st.error('Please enter a valid maximum number')

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

        st.session_state.yaml_string = yaml.dump(
            data_to_export, sort_keys=False, allow_unicode=True)
        st.text_area("YAML Output", st.session_state.yaml_string, height=300)

        try:
            # Attempt to generate the SHACL graph
            shacl_out = shaclgen.ShaclGenerator(
                str(st.session_state.yaml_string)).as_graph()
            st.success("SHACL graph generation successful.")
            st.session_state.rdf_test_successfull = True
        except Exception as e:
            # Handle exceptions specific to ShaclGenerator
            st.error(f"An error occurred during SHACL generation: {e}")
            st.session_state.rdf_test_successfull = False

        try:
            # Attempt to generate the OWL graph
            owl_out = owlgen.OwlSchemaGenerator(
                str(st.session_state.yaml_string)).as_graph()
            st.success("OWL graph generation successful.")
            st.session_state.rdf_test_successfull = True
        except Exception as e:
            # Handle exceptions specific to OwlSchemaGenerator
            st.error(f"An error occurred during OWL generation: {e}")
            st.session_state.rdf_test_successfull = False

if st.session_state.rdf_test_successfull:

    st.text("")
    st.divider()

    st.header('Add Overlays to SemanticDataLink')

    # Create Capture Base ID
    try:
        st.session_state.said = generate_said(yaml_str)
        st.success('Capture Base ID successfully generated')
        st.code(f'''{st.session_state.said}''', language="python")
    except:
        st.error('Error while compiling Capture Base ID')
    st.divider()
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
    files = glob.glob("oca/overlays/*.json")
    options = {
        "Morphologic": [x for x in files if x.split('/')[-1].split('_')[0] == 'morphology'],
        "Semantic": [x for x in files if x.split('/')[-1].split('_')[0] == 'semantic'],
        "Pragmatic": [x for x in files if x.split('/')[-1].split('_')[0] == 'pragmatic']
    }
    st.write(f"""**:blue[Morphologic: {len(options['Morphologic'])} files 
             --- Semantic: {len(options['Semantic'])} files
             --- Pragmatic: {len(options['Pragmatic'])} files]**""")

    # Multiselect widget to choose options
    user_inputs = {}
    options_multiselect = st.multiselect("Select Options", options, options)
    count = 0
    for option in options_multiselect:
        # Add top-level key to dict
        user_inputs[option] = {}
        with st.expander(option):
            # Dictionary to keep track of checkbox states
            checkbox_states = {}
            for overlay in options[option]:
                checkbox_states[overlay] = st.checkbox(
                    f'{overlay.split("/")[-1]}')
            for checkbox, is_checked in checkbox_states.items():
                if is_checked:
                    user_inputs[option][checkbox] = {}
                    st.subheader(checkbox)
                    with open(checkbox) as json_file:
                        my_dict = dict(json.load(json_file))
                        my_dict['capture_base'] = st.session_state.said
                    st.write(my_dict)

                    # Dictionary to store user inputs
                    for key, val in my_dict.items():
                        # Prevent capture base id from changes
                        if key == 'capture_base':
                            json_input = st.text_area(
                                f":red[{key}] set programatically:",
                                key=count,
                                value=json.dumps(val),
                                disabled=True
                            )
                            # st.write(f'Capture Base ID: --- {said} ---')
                        # If key == 'type' or 'language' set default values
                        if key == 'type' or key == 'language':
                            json_input = st.text_area(
                                f"Enter value for :red[{key}] in JSON format:",
                                key=count,
                                value=json.dumps(val)
                            )
                        if key != 'type' and key != 'language' and key != 'capture_base':
                            # User inputs JSON data for each key
                            json_input = st.text_area(
                                f"Enter value for :red[{key}] in JSON format:", key=count)
                        try:
                            # Parse the JSON input
                            user_inputs[option][checkbox][key] = json.loads(
                                json_input)
                            st.success(
                                f'Input saved --- (  {json_input}  )')
                        except json.JSONDecodeError:
                            if json_input:  # Only show an error if the user has entered something
                                st.error(
                                    f"Invalid JSON format for {key}")
                        except:
                            st.error('Other Error')

                        # Increaae counter
                        count += 1

    st.divider()
    st.divider()

    # # Function to serialize a graph and add it to a ZIP file
    # def add_graph_to_zip(zipfile_obj, graph, filename):
    #     # Serialize the graph to Turtle format
    #     ttl_data = graph.serialize(format='turtle')
    #     zipfile_obj.writestr(filename, ttl_data)

    # # Create a ZIP file in memory
    # zip_buffer = BytesIO()
    # with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
    #     add_graph_to_zip(zip_file, shacl_out, 'shacl_graph.ttl')
    #     add_graph_to_zip(zip_file, owl_out, 'owl_graph.ttl')

    # # Prepare the ZIP file for downloading
    # zip_buffer.seek(0)
    # zip_bytes = zip_buffer.getvalue()

    # st.download_button(label="Download Graphs (SHACL and OWL)",
    #                    data=zip_bytes,
    #                    file_name="graphs.zip",
    #                    mime="application/zip")
