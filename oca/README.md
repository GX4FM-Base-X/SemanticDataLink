# OVA - Overlays Capture Architecture



The Overlays Capture Architecture (OCA) is a sophisticated framework that offers a comprehensive approach for managing and representing data objects and their relationships. At its core, OCA enables the explicit representation of task-specific objects that are deterministically related to each other. This system allows for the creation of "Overlays," which add contextual depth and specific semantic tasks to a base object, known as a "Capture Base." These Overlays, when combined, offer a rich and nuanced understanding of the data object, enhancing its semantic interoperability and utility across various applications.

<!-- TOC -->

- [OVA - Overlays Capture Architecture](#ova---overlays-capture-architecture)
    - [Overlays](#overlays)
        - [Concept and Function of Overlays in OCA:](#concept-and-function-of-overlays-in-oca)
        - [Types and Quantity of Overlays:](#types-and-quantity-of-overlays)
    - [OCA & LinkML](#oca--linkml)
        - [Suggested Technical Approach:](#suggested-technical-approach)
- [Usage](#usage)
- [Semantic Data Link Streamlit UI](#semantic-data-link-streamlit-ui)
    - [Code Overview](#code-overview)
    - [Run](#run)
        - [Using the Streamlit UI](#using-the-streamlit-ui)
        - [Usage with Docker](#usage-with-docker)

<!-- /TOC -->

1. **Content-Driven Structure**: OCA utilizes immutable objects supported by Self-Addressing Identifiers (SAIDs). These identifiers are cryptographically bound to the content, ensuring security and portability. The immutable nature of these objects means they cannot be altered once created, providing a stable foundation for data representation.

2. **Simplified Data Pooling**: With OCA, decoupling of data can happen at any moment, as overlays are linked objects. This capability allows for the seamless combination of data from various sources.

3. **Stable Capture Base**: Extensions and modifications are applied through overlays, simplifying the process of updating data objects without the need to reissue the entire capture base.

4. **Flagged Attributes and Encryption**: Attributes within the capture base that could potentially reveal the identity of a governing entity can be flagged for encryption, enhancing data privacy and security.

5. **Decentralized Semantics**: OCA employs a decentralized approach to semantics, separating definitional and contextual tasks into specific objects, thereby enhancing the digital representation of complex objects.

6. **Data Types and Overlays**: OCA supports various data types like Reference, Boolean, Binary, DateTime, and Arrays. Overlays are used to add layers of information to a Capture Base, enabling metadata addition, information display transformation, and custom data processing guidance.

7. **Internationalization and Data Validation**: OCA supports different language encodings, ensuring that a single report definition can include various attribute forms for different languages. It also ensures that data records are compliant with OCA bundle schema.

## Overlays

The concept and function of overlays within the Overlays Capture Architecture (OCA) framework are central to its design and utility. Overlays are essentially additional layers of information that can be applied to a base data object, known as a Capture Base, to extend or enhance its meaning, context, or functionality.

### Concept and Function of Overlays in OCA:

1. **Enhancing Data Context and Meaning**: Overlays provide supplementary context or definitions to a Capture Base. This enables users to understand not just the data itself, but also its relevance, application, or implications in various scenarios.

2. **Modularity and Flexibility**: Overlays allow for a modular approach to data structuring. You can add or modify Overlays without altering the underlying Capture Base, making the system highly adaptable to changing requirements.

3. **Interoperability and Reusability**: By standardizing the way additional information is attached to data objects, Overlays facilitate interoperability between different systems and encourage the reuse of established data models.

### Types and Quantity of Overlays:
<!-- TOC -->

- [OVA - Overlays Capture Architecture](#ova---overlays-capture-architecture)
    - [Overlays](#overlays)
        - [Concept and Function of Overlays in OCA:](#concept-and-function-of-overlays-in-oca)
        - [Types and Quantity of Overlays:](#types-and-quantity-of-overlays)
    - [OCA & LinkML](#oca--linkml)
        - [Suggested Technical Approach:](#suggested-technical-approach)
- [Usage](#usage)

<!-- /TOC -->
There isn't a fixed number of Overlays in OCA; rather, the framework is designed to support the creation and integration of as many Overlays as needed for a particular application or domain. This extensibility is a key feature of OCA, allowing it to be tailored to a wide range of use cases.

## OCA & LinkML

Combining Overlays Capture Architecture (OCA) with LinkML (Linked Data Modeling Language) can create a powerful framework for managing and representing complex data structures, especially in scenarios where data interoperability and schema reusability are crucial. LinkML is a language for modeling linked data, particularly useful for defining schemas for knowledge graphs, databases, and API payloads.

### Suggested Technical Approach:

1. **Define Base Schemas in LinkML**: Utilize LinkML to define the base schemas which correspond to the Capture Bases in OCA. These schemas would include the fundamental attributes of the data objects and their relationships.

2. **Use LinkML for Semantic Layering**: Extend the LinkML schemas to include semantic layers that describe the context and use of the data, akin to OCA's Overlays. This can include additional properties, constraints, and relationships that provide a deeper understanding of the data.

3. **Data Transformation and Validation**: Use LinkML's tools for data transformation and validation in conjunction with OCA's data validation capabilities. This ensures that the data adheres to the defined schemas and overlays, maintaining consistency and quality.

# Usage

# Semantic Data Link Streamlit UI

This repository contains the code for a Streamlit-based web application designed to facilitate the creation and management of metadata attributes for datasets.

## Code Overview

The Python script `SemanticDataLink.py` sets up a Streamlit UI where users can:

- Add and remove metadata attributes dynamically.
- Input basic information such as Main Identifier, ID, and Name, which are essential for the creation of LinkML documents.
- Manage prefixes for the attributes' URIs.
- Customize each attribute with properties like multivalued, identifier, required, datatype, and more.
- Provide specific ranges, patterns, and slot URIs for attributes.
- Define enums and their permissible values, including descriptions and meanings.
- Generate LinkML schema documents and export them in YAML, SHACL, and OWL formats.

## Run

To run the application locally, follow these steps:

1. Clone the repository and navigate to the directory containing `SemanticDataLink.py`.
2. Ensure you have Python and Streamlit installed. For an easy setup you can use our `requirements.txt` file. Simply create a python environment `python3 -m venv venv` activate this environment `source venv/bin/activate` (in root of repository) and install allpackages `pip install -r requirements.txt`.
3. Run the command: `streamlit run SemanticDataLink.py`.
4. The web application will open in your default browser.

### Using the Streamlit UI

1. Fill in the "Basic Information" section with the Main Identifier, ID, and Name.
2. Add or delete prefixes as necessary.
3. Use the "Add Attribute" and "Delete Last Attribute" buttons to manage your attributes list.
4. Customize each attribute's properties using the provided fields and checkboxes.
5. Proceed identically by selection additional overlays.
6. Once all attributes and overlays are configured, you can generate the LinkML schema by toggling the 'Generate LinkML Schema' switch.
7. Copy or download the SHACL and OWL Graphs.

### Usage with Docker

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
