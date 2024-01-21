# SemanticDataLink

SemanticDataLink is an innovative approach to achieve semantic interoperability in diverse data spaces. Our goal is to provide a robust framework that facilitates seamless integration and understanding across various data formats and structures, ensuring that data from different sources can be effectively combined and utilized.

## Overview

In the era of big data, the ability to integrate information from disparate sources is crucial. SemanticDataLink is designed to address the challenges of semantic interoperability by providing tools and methodologies to link data semantically. Our solution emphasizes on standardization, data harmonization, and the use of advanced semantic technologies to make data more accessible and useful.

## Features

- **Data Standardization**: Enforces common standards for data formatting and structure.
- **Semantic Mapping**: Utilizes ontologies and schema mappings to establish meaningful connections between different data sets.
- **Query Expansion**: Enhances data retrieval capabilities through semantically enriched query processes.
- **API Integration**: Offers a robust API for seamless integration with existing systems.
- **Data Harmonization**: Aligns disparate data sources for coherent analysis and interpretation.

## Introduction

Semantic Data Link is a Streamlit-based web application designed to facilitate the handling and management of schema-based data structures, particularly focusing on the integration of LinkML (Linked Data Modeling Language) schemas. The application allows users to upload, validate, and augment data schemas using LinkML, and provides a user-friendly interface for adding overlays to these schemas.

## Features

1. **Import Stable Capture Base (SCB):** Users can upload YAML files representing their data schemas. The application validates the YAML content, converts it to JSON, and displays it.

2. **Validation Against LinkML Schema:** Users can validate JSON data against the uploaded LinkML schema to ensure compliance.

3. **Capture Base ID Generation:** The app generates a unique ID for each Capture Base, aiding in tracking and referencing.

4. **Add Overlays to SCB:** Users can enhance their schemas with overlays. Overlays are additional data layers that provide extra context or definitions to the base schema. The app supports adding various types of overlays (e.g., Morphologic, Semantic, Pragmatic) and ensures that they are correctly bound to the Capture Base.

5. **Database Integration:** The processed Capture Bases and overlays can be saved to a database for persistent storage and management.

6. **Interactive UI:** The application uses Streamlit’s widgets for a dynamic and interactive user experience, making it easy to input, validate, and manage schema data.

## How to Use

1. **Launch the Application:** Run the Streamlit app by executing the provided Python script.

2. **Upload a Schema:** Use the file uploader to import a YAML file representing your data schema. The application will validate and convert it to JSON.

3. **Validate Data:** Optionally, validate JSON data against the uploaded schema. Input the JSON data and specify the class it should adhere to within the schema.

4. **Generate Capture Base ID:** The application will automatically generate an ID for the uploaded schema.

5. **Add Overlays:** Enhance your schema with additional overlays. Select from available types and input the necessary data.

6. **Review and Save:** Review the final schema with overlays and save it to the database.

7. **Download or Use Data:** The final augmented schema can be downloaded or directly used within the application for further data operations.

## Overlay Overview / Description

**TODO!** 
[oca/overlays/README.md](oca/overlays/README.md)

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

Your Name - [maximilian.staebler@dlr.de](mailto:maximilian.staebler@dlr.de)

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