# SemanticDataLink

SemanticDataLink is an innovative approach to achieve semantic interoperability in diverse data spaces. Our goal is to provide a robust framework that facilitates seamless integration and understanding across various data formats and structures, ensuring that data from different sources can be effectively combined and utilized.

**Overview**

In the era of big data, the ability to integrate information from disparate sources is crucial. SemanticDataLink is designed to address the challenges of semantic interoperability by providing tools and methodologies to link data semantically. Our solution emphasizes on standardization, data harmonization, and the use of advanced semantic technologies to make data more accessible and useful.

Semantic Data Link is a Streamlit-based web application designed to facilitate the handling and management of schema-based data structures, particularly focusing on the integration of LinkML (Linked Data Modeling Language) schemas. The application allows users to upload, validate, and augment data schemas using LinkML, and provides a user-friendly interface for adding overlays to these schemas.

For more information on the SemanticDataLink approach please refer to [oca/README.md](oca/README.md)

## Usage

### Semantic Data Link Streamlit UI

This repository contains the code for a Streamlit-based web application designed to facilitate the creation and management of metadata attributes for datasets.

### Code Overview

The Python script `SemanticDataLink.py` sets up a Streamlit UI where users can:

- Add and remove metadata attributes dynamically.
- Input basic information such as Main Identifier, ID, and Name, which are essential for the creation of LinkML documents.
- Manage prefixes for the attributes' URIs.
- Customize each attribute with properties like multivalued, identifier, required, datatype, and more.
- Provide specific ranges, patterns, and slot URIs for attributes.
- Define enums and their permissible values, including descriptions and meanings.
- Generate LinkML schema documents and export them in YAML, SHACL, and OWL formats.

### Run

To run the application locally, follow these steps:

1. Clone the repository and navigate to the directory containing `SemanticDataLink.py`.
2. Ensure you have Python and Streamlit installed. For an easy setup you can use our `requirements.txt` file. Simply create a python environment `python3 -m venv venv` activate this environment `source venv/bin/activate` (in root of repository) and install allpackages `pip install -r requirements.txt`.
3. Run the command: `streamlit run SemanticDataLink.py`.
4. The web application will open in your default browser.

#### Using the Streamlit UI

1. Fill in the "Basic Information" section with the Main Identifier, ID, and Name.
2. Add or delete prefixes as necessary.
3. Use the "Add Attribute" and "Delete Last Attribute" buttons to manage your attributes list.
4. Customize each attribute's properties using the provided fields and checkboxes.
5. Proceed identically by selection additional overlays.
6. Once all attributes and overlays are configured, you can generate the LinkML schema by toggling the 'Generate LinkML Schema' switch.
7. Copy or download the SHACL and OWL Graphs.

#### Usage with Docker

To use the application with Docker, you need to have Docker installed and running on your machine. For more information about docker checkout the foler [/docker](/docker/)

1. Build the Docker image from the Dockerfile in the repository:

```bash
docker build -t semanticdatalink .
```

2. Run a container from the image:
```bash
docker run --rm -p 8501:8501 --name semanticdatalink  semanticdatalink
```
Keep in mind that `--rm` will delete the container after exit. If you want to keep the container simply remove `--rm` from command.

3. Access the application through http://localhost:8501 in your web browser.
Remember to mount the necessary volumes if you need to access files from your host system in the Streamlit application.


## Requirements

- Python 3.x
- Streamlit
- PyMongo
- PyYAML
- LinkML
- Additional dependencies as listed in `requirements.txt`

## Installation

1. Install Python and Pip.
2. Clone the repository or download the script.
3. **CHANGE / DELETE OR ADD `.streamlit/secrets.toml` TO `.gitignore` IF YOU ADD SECRET VALUES!**
4. Install dependencies: `pip install -r requirements.txt`.
5. Run the Streamlit app: `streamlit run [script_name].py` - here: `streamlit run oca_ui.py`.

## Docker

Please refer to `docker/SemanticDataLink/README.md`

**Important:**

If you want to use a database for storing all files (mongodb) please refer to [docker/mongodb](docker/mongodb). 

## Contributing

Contributions are what make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

## Contact

Maximilian Stäbler (German Aerospace Center - Institute for AI Safety & Security) - [maximilian.staebler@dlr.de](mailto:maximilian.staebler@dlr.de)

<!-- ---

This README provides a basic outline that you can customize based on the specific needs and features of your project. It includes sections like an overview of the project, features, installation and usage instructions, contribution guidelines, license information, and contact details.




1. **Morphological (Structural) Attributes**:
   - **Format**: Specifies the data format, such as CSV, JSON, XML, etc.
   - **Cardinality**: Indicates the number of elements in a dataset or the number of unique values in a column.
   - **Dimensionality**: Refers to the number of dimensions in a dataset, like rows and columns in a 2D dataset.
   - **Encoding**: Describes the method used to represent data, such as UTF-8 for text.
   - **Size**: The physical size of the dataset, often in terms of storage space (e.g., megabytes).

2. **Semantic (Definitional) Attributes**:
   - **Data Type**: Indicates the type of data (integer, string, boolean, etc.).
   - **Unit**: Specifies the measurement unit (e.g., meters, seconds, dollars).
   - **Validity Rules**: Rules that define valid data entries (e.g., a positive integer, a string of a certain length).
   - **Label/Name**: The name or label assigned to a particular data element or feature.
   - **Metadata**: Information describing data, such as source, author, creation date.

3. **Pragmatic (Contextual) Attributes**:
   - **Usage Frequency**: How often the data is accessed or used.
   - **Access Control**: Information about who can access or modify the data.
   - **Relevance**: The significance of the data in a given context.
   - **Source Credibility**: The trustworthiness or reliability of the data source.
   - **Standard/Regulation Compliance**: Whether the data adheres to specific standards or regulations (e.g., GDPR for personal data).

----

1. **Morphological (Structural) Attributes**:
   - **Type and Classification**: These attributes define the schema object type and its classification, providing a structural base for data categorization.
   - **Attribute Name and Type**: Found in the Capture Base, these define the names and data types (e.g., Text, Numeric, Boolean) of attributes.
   - **Flagged Attributes**: Attributes marked for their potential sensitivity, indicating structural considerations for data protection.
   - **Format**: Specified in the Format Overlay, this determines the structure of data fields, like defining regular expressions for text or MIME types for binary data.
   - **Cardinality**: Defined in the Cardinality Overlay, it specifies the number of values an attribute can have, indicating the structural limitations or capacities of data fields.
   - **Attribute Mapping**: In the Attribute Mapping Overlay, this shows relationships between attributes in different data models, reflecting structural connections between data sets.

2. **Semantic (Definitional) Attributes**:
   - **Attribute Information**: Found in the Information Overlay, this provides detailed descriptions of each attribute, adding meaning and context.
   - **Language**: Used in various overlays, it defines the language of metadata, enhancing understanding and interpretation.
   - **Character Encoding**: In the Character Encoding Overlay, this specifies how characters are represented digitally, impacting how data is interpreted and displayed.
   - **Standard**: The Standard Overlay defines technical specifications or agreements used to format and manage data.
   - **Meta Information**: Including schema name and description in the Meta Overlay, these attributes provide an overarching context and definition for the data schema.

3. **Pragmatic (Contextual) Attributes**:
   - **Conformance**: Specified in the Conformance Overlay, this indicates whether data entry for each attribute is mandatory or optional, guiding practical data entry processes.
   - **Entry Codes and Entries**: Defined in Entry Code and Entry Overlays, these provide pre-defined values for attributes, guiding practical data interpretation and usage.
   - **Units and Unit Mapping**: In the Unit and Unit Mapping Overlays, these define measurement units, essential for practical application and data interpretation in real-world contexts.
   - **Sensitive Attributes**: Identified in the Sensitive Overlay, these attributes need special handling due to privacy or ethical considerations, influencing how data is treated in practical scenarios.
   - **Subset and Transformation**: The Subset and Transformation Overlays define subsets of attributes and transformations for data, relevant for practical applications and specific use cases.

These attributes collectively ensure that data managed by the OCA framework is well-structured, meaningful, and contextually relevant, supporting its effective use in various applications. -->