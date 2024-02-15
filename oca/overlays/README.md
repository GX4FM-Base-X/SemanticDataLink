# Overlays - Metadata Attributes YAML Directory

This directory contains YAML files for each metadata attribute used in the Semantic Data Link Streamlit application. These files define the properties and constraints for metadata attributes associated with datasets to ensure comprehensive descriptions and facilitate data interoperability.

## Overview

Each YAML file is structured to represent a single metadata attribute with specific properties that define its characteristics and constraints. These properties can include the datatype range, whether the attribute is multivalued or required, and any specific patterns that the attribute's value must match.

## Files

The YAML files included in this directory are:

- `UsageFrequency.yaml`
- `Conformance.yaml`
- `Information.yaml`
- `Unit.yaml`
- `Label.yaml`
- `Standard.yaml`
- `Domain.yaml`
- `Keywords.yaml`
- `Encoding.yaml`
- `Cardinality.yaml`
- `Dimensionality.yaml`
- `Size.yaml`

Each file corresponds to one of the metadata attributes that can be customized within the Streamlit application.

## Usage

These YAML files are used by the Streamlit application to render the UI dynamically. Users can add or modify metadata attributes, which are then saved in this format.

To use these YAML files:

1. Place them in the appropriate directory as specified by the Streamlit application.
2. Run the application, and it will automatically load the attributes from these files.
3. You can add or remove attributes by interacting with the UI or by modifying these YAML files directly.

## Contributing

Contributions to these YAML files are welcome. Please ensure that you follow the established file format and include a description of the attribute and its properties in your pull requests.

## Contact
For any further questions or requests, please file an issue in the repository, and we will get back to you promptly.