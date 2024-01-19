import streamlit as st
import pymongo
import yaml
import io
from linkml_runtime.dumpers import json_dumper
from linkml.validator import validate
from helpers import *
import glob

st.set_page_config(layout="wide")

st.title('Semantic Data Link')

st.header('Import Stable Capture Base (SCB)')
st.markdown('''
            A Capture Base is the purest and simplest form of a schema, 
            defining the structural characteristics of a dataset. 
            It is the foundational layer upon which to bind task-specific objects to enhance the meaning of inputted data.
''')

# File uploader
uploaded_file = st.file_uploader(
    "Choose a file (yaml / yml only!)", type=['yaml', 'yml'])

FILE_VALID = False
if uploaded_file is not None:
    # Read the content of the file
    content = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    yaml_content = yaml.safe_load(content)
    st.success("File is contains valid YAML. Converting to JSON...")
    try:
        # Check if the YAML file has the required structure
        linkml_json = json_dumper.dumps(yaml_content)
        linkml_dict = json.loads(linkml_json)
        st.success("Convertion to JSON successful.")
        FILE_VALID = True

    except yaml.YAMLError as e:
        st.error("Error parsing YAML file. Please ensure it is a valid LinkML YAML.")

    on = st.toggle('Show caputure Base')
    if on:
        st.json(linkml_json)

if FILE_VALID:
    on = st.toggle('Do you want to check your data against the LinkML schema?')
    if on:
        # Input text to be validated
        txt_validate = st.text_area(
            'Insert JSON that you want to validate.'
        )
        # Explicitly define class thats will be validated
        txt_class = st.text_input(
            'Please explicitly specifies which class within the schema (i.e. Person) the data instance should adhere to.!'
        )
        # Start validation
        if st.button('Validate', type="primary"):
            try:
                txt_json = dict(json.loads(txt_validate))
            except json.JSONDecodeError:
                # Display error message if conversion fails
                st.error("Invalid JSON. Please enter a valid JSON string.")
            # Validate Input
            report = validate(txt_json, yaml_content, txt_class)
            if not report.results:
                st.success('JSON Input Valid!')
            else:
                for result in report.results:
                    st.error(result.message)

    st.divider()
    # Create Capture Base ID
    try:
        said = generate_said(linkml_json)
        st.success('Capture Base ID successfully generated')
        st.code(f'''{said}''', language="python")
    except:
        st.error('Error while compiling Capture Base ID')
    st.divider()

    st.header('Add Overlays to SCB')
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
                        my_dict['capture_base'] = said
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

    if st.button("Generate & Download", key='generator', type='primary'):
        # Check all keys if they have manually entered values.
        # If yes, print them and use it for generating the output.
        # If not these keys will be neglected
        keys_to_delete = []
        for top_key in user_inputs.keys():
            for middle_key, middle_value in user_inputs[top_key].items():
                field_count = count_keys_except(
                    user_inputs[top_key][middle_key]
                )
                if field_count < 1:
                    keys_to_delete.append((top_key, middle_key))
                    # user_inputs[top_key][middle_key]
                    st.write(field_count)

        # Delete identified sub-dictionaries
        for key in keys_to_delete:
            del user_inputs[key[0]][key[1]]

        st.write("Submitted Data:")
        st.json(user_inputs)

        # Add all data to database
        # Insert Capture Base
        capture_base_status = insert_capture_base(linkml_dict, said)
        if capture_base_status == 1:
            st.warning(
                f"Capture Base **_{said}_** already exists!")
        if capture_base_status == -1:
            st.error(
                f'Capture Base **_{said}_** could not be written to database')

        # Insert all overlays
        for top_key in user_inputs.keys():
            for middle_key, middle_value in user_inputs[top_key].items():
                overlay_said = generate_said(user_inputs[top_key][middle_key])
                overlay_status = insert_overlay(
                    user_inputs[top_key][middle_key],
                    overlay_said
                )
                if overlay_status == -1:
                    st.error(
                        f'Item with `capture_base` **_{overlay_said}_** could not be written to database'
                    )
                if overlay_status == 1:
                    st.warning(
                        f"Overlay **_{said}_** already exists"
                    )
        if capture_base_status == 0 and overlay_status == 0:
            st.success(
                f"Capture Base **_{said}_** and overlays successfuly written to database!")
