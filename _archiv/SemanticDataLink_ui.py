from helpers import *

#################################
# Streamlit settings
st.set_page_config(layout="wide")
st.title('Semantic Data Link')
# Predefined Attributes
if 'PREFIXES' not in st.session_state:
    st.session_state.PREFIXES = {"linkml": "https://w3id.org/linkml/"}
if 'ADD_OVERLAYS' not in st.session_state:
    st.session_state.ADD_OVERLAYS = {}
if 'GRAPHS_SUCCESS' not in st.session_state:
    st.session_state.GRAPHS_SUCCESS = False
if 'SAID' not in st.session_state:
    st.session_state.SAID = {}
if 'VALIDATOR' not in st.session_state:
    st.session_state.VALIDATOR = False
if 'LINKML_SCHEMA' not in st.session_state:
    st.session_state.LINKML_SCHEMA = {}

# Predefined datatypes for selection
PREDEFINED_DATATYPES = ["string", "integer", "float", "boolean", "date", "enum", "datetime", "decimal", "double",
                        "HttpsIdentifier", "uri"]
#################################

# LinkML already exists -- Uploader
FILE_AVAILABLE = st.toggle(
    'Do you have an LinkML Schema file and want to upload it?', disabled=True)
if FILE_AVAILABLE:
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file (yaml / yml only!)", type=['yaml', 'yml'])

    FILE_VALID = False
    if uploaded_file is not None:
        # Read the content of the file
        content = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        try:
            yaml_content = yaml.safe_load(content)
            FILE_VALID = True
            st.success("File is contains valid YAML.")
        except yaml.YAMLError as e:
            st.error(
                "Error parsing YAML file. Please ensure it is a valid LinkML YAML.")

        on = st.toggle('Show caputure Base')
        if on:
            # Convert the Python data back to a pretty-printed YAML string
            pretty_yaml_str = yaml.dump(
                yaml_content, sort_keys=False, indent=2)

            # Display the pretty-printed YAML in the Streamlit UI
            st.text_area("YAML Content", pretty_yaml_str, height=300)

# General Information of YAML File
st.subheader("General Information")
main_prefix = st.text_input(
    "Main Identifier", value="https://base-x-ecosystem.com/")
dataset_id = st.text_input("ID", placeholder="base-schema")
if dataset_id == '':
    st.error(
        f':red[General Information -- ID] field is mandatory. Please choose a suitable ID for the Entity')
dataset_name = st.text_input("Name", placeholder="yourSchemaName")
if dataset_name == '':
    st.error(
        f':red[General Information -- Name] field is mandatory. Please choose a suitable name for the Entity')

st.divider()

st.subheader("Prefixes")
for key, value in st.session_state.PREFIXES.items():
    st.text(f"{key}: {value}")

prefix_key = st.text_input("Add Prefix (Key)", placeholder="linkml")
prefix_value = st.text_input(
    "Add Prefix (Value)", placeholder="https://w3id.org/linkml/")
if st.button('Add Prefix'):
    if prefix_key and prefix_value:
        st.session_state.PREFIXES[prefix_key] = prefix_value
        st.rerun()

# Delete global variable
deletable_keys = list(st.session_state.PREFIXES.keys())
deletable_keys.remove('linkml')
delete_var_key = st.selectbox(
    "Delete Global Variable", [''] + deletable_keys)
if st.button('Delete Selected Prefix'):
    if delete_var_key and delete_var_key in st.session_state.PREFIXES:
        del st.session_state.PREFIXES[delete_var_key]
        st.rerun()

st.divider()

# Initialize the session state for managing attributes if it doesn't already exist
if 'attributes' not in st.session_state:
    st.session_state.attributes = []
if 'enums' not in st.session_state:
    st.session_state.enums = {}

# Function to add a new attribute to the session state


def refresher():
    st.rerun()


def add_attribute():
    st.session_state.attributes.append(
        {'name': '', 'multivalued': '', 'required': '', 'pattern': ''})
# Function to delete the last attribute from the session state


def delete_last_attribute():
    if st.session_state.attributes:
        st.session_state.attributes.pop()


# Layout for add and delete buttons
col1, col2, _, _, _ = st.columns(5)
with col1:
    st.button("Add Attribute", on_click=add_attribute,
              type='primary', key='add_top')
with col2:
    st.button("Delete Last Attribute",
              on_click=delete_last_attribute, key='delete_top')

# Display input fields for each attribute and its parameters
for idx, attribute in enumerate(st.session_state.attributes):
    with st.container():
        # Name attribute
        st.markdown(f'**Attribute {idx + 1}**')

        col1, col2 = st.columns([4, 1])
        col3, col4 = st.columns([1, 3])
        col5, col6 = st.columns([2, 2])
        col7, col8 = st.columns([2, 2])
        col9, col10 = st.columns([1, 3])

        with col1:
            attribute['name'] = st.text_input(
                f":red[Name]*", value=attribute['name'], key=f"name_{idx}")
            if attribute['name'] == "":
                st.error(f':red[Name] can not be empty')
        with col2:
            attribute['multivalued'] = st.checkbox(
                f"Multivalued", key=f"multivalued_{idx}", on_change=refresher)
            attribute['required'] = st.checkbox(
                f"Required", key=f"required_{idx}", on_change=refresher)
            attribute['pattern_check'] = st.checkbox(
                f"Pattern", key=f"pattern_check_{idx}", on_change=refresher)

        with col3:
            attribute['range'] = st.selectbox(f":red[Range]*", PREDEFINED_DATATYPES, index=PREDEFINED_DATATYPES.index(attribute.get(
                'range', 'int')) if attribute.get('range', 'int') in PREDEFINED_DATATYPES else 0, key=f"range_{idx}", on_change=refresher)
            if attribute['range'] == 'enum':
                with col4:
                    # Text input for new enum name
                    enum_name = st.text_input("Enter enum name:")
                    attribute['enums'] = {}

                    # Text area for enum values (comma-separated)
                    enum_description = st.text_area("Enter enum description:")
                    enum_meaning = st.text_area(
                        "Enter enum meaning (ontology / class ie.: PATO:0001421):")

                    if enum_name and enum_description and enum_meaning:
                        st.session_state.enums[enum_name] = {
                            'description': enum_description,
                            'meaning': enum_meaning
                        }
                        attribute['enums'][enum_name] = {
                            'description': enum_description,
                            'meaning': enum_meaning
                        }
                    st.divider()
                    # Make it possible to delete enum
                    deletable_keys = list(st.session_state.enums.keys())
                    delete_var_key = st.selectbox(
                        "Delete Enum", [''] + deletable_keys)
                    if st.button('Delete Selected Enum'):
                        if delete_var_key and delete_var_key in st.session_state.enums:
                            del st.session_state.enums[delete_var_key]

                    # Print enums
                    st.json(st.session_state.enums)

            if attribute['range'] == "integer" or attribute['range'] == "float" or attribute['range'] == "decimal" or attribute['range'] == "double":
                with col4:
                    attribute['minimum_value'] = st.text_input(
                        "Minimum Value:", key=f"minimum_number_{idx}")
                    if contains_number(attribute['minimum_value']) == False:
                        st.error('Please enter a valid number')
                    attribute['maximum_value'] = st.text_input(
                        "Maximum Value:", key=f"maximum_number_{idx}")
                    if contains_number(attribute['maximum_value']) == False:
                        st.error('Please enter a valid number')

        with col5:
            prefix_selection = st.selectbox(
                f"Slot_URI", ['None'] + list(st.session_state.PREFIXES.keys()), key=f"prefix_selection_{idx}", on_change=refresher)
            if prefix_selection != 'None':
                with col6:
                    slot_uri_value = st.text_input(
                        f"Value:", placeholder='<class / attribute>', key=f"slot_uri_{idx}")
            if prefix_selection != 'None' and slot_uri_value != "":
                st.write(f"{prefix_selection} : {slot_uri_value}")

            attribute['slot_uri'] = f"{prefix_selection}:{slot_uri_value}" if prefix_selection != 'None' else ''

        if attribute['pattern_check']:
            with col7:
                attribute['pattern'] = st.text_input(
                    "Pattern for Data Validation [regex]:", key=f"pattern_{idx}", on_change=refresher)
            with col8:
                pattern_regex_test = st.text_input(
                    "Pattern Test:", key=f"pattern_test_{idx}", on_change=refresher)
                if pattern_regex_test != '':
                    if pattern_test(pattern_regex_test, attribute['pattern']):
                        st.success('Valid Input String')
                    else:
                        st.error('String does not match pattern')
        elif not attribute['pattern_check']:
            attribute['pattern'] = ''

        # Description
        with col9:
            description_checkbox = st.checkbox(
                f"Add Description", key=f"description_checkbox_{idx}", value=attribute.get(
                    'description_checkbox', ''), on_change=refresher)
        if description_checkbox:
            with col10:
                attribute['description'] = st.text_input(
                    "Attribute description (free text):", key=f"description_{idx}", value=attribute.get(
                        'description', ''), on_change=refresher)
    # st.subheader(f"Attribute {i + 1}")
    # attribute['name'] = st.text_input(
    #     f"Name {i + 1}", key=f"name_{i}", value=attribute['name'])
    # attribute['type'] = st.selectbox(f"Type {i + 1}", ['String', 'Integer', 'Float', 'Boolean'], key=f"type_{i}", index=[
    #                                  'String', 'Integer', 'Float', 'Boolean'].index(attribute['type']) if attribute['type'] in ['String', 'Integer', 'Float', 'Boolean'] else 0)
    # attribute['description'] = st.text_area(
    #     f"Description {i + 1}", key=f"description_{i}", value=attribute['description'])

                # enums noch aufnehmen: bisher nicht in attribute

# Layout for add and delete buttons
if len(st.session_state.attributes) > 2:
    col1, col2, _, _, _ = st.columns(5)
    with col1:
        st.button("Add Attribute", on_click=add_attribute,
                  key='add_end', type='primary')
    with col2:
        st.button("Delete Last Attribute",
                  on_click=delete_last_attribute, key='delete_end')

st.text("")
st.divider()

# Export and Validate
st.session_state.VALIDATOR = st.toggle(
    'Validate LinkML and add Overlays')
if st.session_state.VALIDATOR:
    valid, report = validate_linkml(
        main_prefix, dataset_id, dataset_name, st.session_state.attributes, st.session_state.PREFIXES)

    st.session_state.LINKML_SCHEMA = parse_linkml(
        main_prefix, dataset_id, dataset_name, st.session_state.attributes, st.session_state.PREFIXES)

    if not valid:
        for k, v in report.items():
            st.error(v)
    else:
        try:
            # Attempt to generate the SHACL graph
            shacl_out = shaclgen.ShaclGenerator(
                str(st.session_state.LINKML_SCHEMA)).as_graph()
            st.success("SHACL graph generation successful.")
            st.session_state.GRAPHS_SUCCESS = True
        except Exception as e:
            # Handle exceptions specific to ShaclGenerator
            st.error(f"An error occurred during SHACL generation: {e}")
            st.session_state.GRAPHS_SUCCESS = False

        try:
            # Attempt to generate the OWL graph
            owl_out = owlgen.OwlSchemaGenerator(
                str(st.session_state.LINKML_SCHEMA)).as_graph()
            st.success("OWL graph generation successful.")
            st.session_state.GRAPHS_SUCCESS = True
        except Exception as e:
            # Handle exceptions specific to OwlSchemaGenerator
            st.error(f"An error occurred during OWL generation: {e}")
            st.session_state.GRAPHS_SUCCESS = False

        # Print LinkML YAML Schema
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_area(
                "YAML Output", st.session_state.LINKML_SCHEMA, height=300)
        with col2:
            st.text_area("OWL", owl_out.serialize(), height=300)
        with col3:
            st.text_area("SHACL", shacl_out.serialize(), height=300)

        if st.session_state.GRAPHS_SUCCESS:
            # if st.session_state.GRAPHS_SUCCESS:
            st.header('SemanticDataLink Overlays')
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
            ''')
            st.divider()
            # Create Capture Base ID
            try:
                st.session_state.SAID = generate_said(
                    st.session_state.LINKML_SCHEMA)
                st.success('Capture Base ID successfully generated')
                st.code(f'''{st.session_state.SAID}''', language="python")
            except:
                st.error('Error while compiling Capture Base ID')
            st.divider()

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
            options_multiselect = st.multiselect(
                "Select Options", options, options)
            count = 0
            for option in options_multiselect:
                # Add top-level key to dict
                user_inputs[option] = {}
                with st.expander(option):
                    # Dictionary to keep track of checkbox states
                    checkbox_states = {}
                    for overlay in options[option]:
                        checkbox_states[overlay] = st.checkbox(
                            f'{overlay.split("/")[-1].split(".")[0]}')

                    for checkbox, is_checked in checkbox_states.items():
                        if is_checked:
                            # user_inputs[option].append(checkbox.split("/")[-1].split(".")[0])
                            # user_inputs[option][checkbox] = {}
                            # st.subheader(checkbox)
                            with open(checkbox) as json_file:
                                my_dict = dict(json.load(json_file))
                                # my_dict['capture_base'] = st.session_state.SAID
                            # st.write(my_dict)

                            # Dictionary to store user inputs
                            for key, val in my_dict.items():
                                # Prevent capture base id from changes
                                # if key == 'capture_base':
                                #     st.write(
                                #         f'{key}: --- {st.session_state.SAID} ---')
                                # if key == 'type' or key == 'language':
                                #     st.write(f'{key}: --- {val} ---')
                                if key != 'type' and key != 'language' and key != 'capture_base':
                                    user_inputs[option][key] = val
                                # try:
                                #     # Parse the JSON input
                                #     user_inputs[option][checkbox][key] = json.loads(
                                #         json_input)
                                #     st.success(
                                #         f'Input saved --- (  {json_input}  )')
                                # except json.JSONDecodeError:
                                #     if json_input:  # Only show an error if the user has entered something
                                #         st.error(
                                #             f"Invalid JSON format for {key}")
                                # except:
                                #     st.error('Other Error')

                            # Increaae counter
                            count += 1

            st.divider()
            st.divider()
            # for checkbox, is_checked in checkbox_states.items():
            #     if is_checked:
            #         st.write(checkbox)

            st.write(user_inputs)


# TODO: Attribute der checkboxen mitaufnehmen. Bisher nur prgamtaic weil der rest überschrieben wird. Muss für alles separat gelten
# Und für jedes Attribut m+üssen die entsprechendne Werte + Datentype aufgenommen werden --> Direkt mit Funktion aus dem ipynb file.

# Jedes Attribut aus dem LinkMl file muss in owl graph und jedes attribut aus dem Overlay in shacl graph
