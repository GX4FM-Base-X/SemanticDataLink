# LinkML

## Introduction to LinkML

Link Model Language (LinkML) is a powerful framework designed to facilitate the creation, maintenance, and deployment of data models across a wide range of domains. At its core, LinkML enables users to define complex data models in a human-readable format, which can then be compiled into various other schema languages including JSON Schema, GraphQL, SQL, and RDF/OWL. This versatility makes LinkML an ideal choice for projects aiming to ensure data consistency, validate data inputs, and streamline the integration between different systems and technologies.

## Key Features

- **Schema Definition**: Define your data models in YAML, making them easy to read, write, and maintain.
- **Multi-Format Compilation**: Compile your LinkML models into multiple output formats to fit the needs of your application or workflow.
- **Validation**: Use generated schemas to validate data, ensuring it conforms to your defined models and business rules.
- **Integration**: Facilitate data integration tasks by leveraging uniform models across different data representation formats.

## Installation

To use LinkML in your project, first, ensure you have Python installed on your system. LinkML can be installed via pip:

```bash
pip install linkml
```

## Getting Started

### Defining a Model

Create a YAML file to define your model. For example, `model.yaml`:

```yaml
id: http://example.org/sample/
name: sample
classes:
  Person:
    description: A person
    slots:
      - id
      - name
      - age
slots:
  id:
    description: unique identifier of a person
    identifier: true
  name:
    description: name of the person
  age:
    description: age of the person
    range: integer
```

### Compiling the Model

To compile your model into a JSON Schema:

```bash
linkml-compile model.yaml --format jsonschema -o model.schema.json
```

### Validating Data Against the Model

Once you have your model compiled, you can use the generated schema to validate your data. For JSON data validation, you can use tools like `jsonschema` in Python.

## Detailed example - suggested usage

```yaml
### More detailed info:
# https://linkml.io/linkml/schemas/index.html
###
id: https://w3id.org/linkml/examples/personinfo # Identifier
name: personinfo # Name of schema
prefixes: # define prefixes --> similar to rdf                                 
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  personinfo: https://w3id.org/linkml/examples/personinfo/
  ORCID: https://orcid.org/
  PATO: http://purl.obolibrary.org/obo/PATO_ # ontology that is used later with ENUMS
default_prefix: personinfo
imports:
  - linkml:types
default_range: string
  
classes: # define class
  Person: # class 
    class_uri: schema:Person             
    slots:   ## specified as a list - details below
     - id
     - full_name
     - aliases
     - phone
     - age
     - status
    id_prefixes:
      - ORCID
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person

# slots are first-class entities in the metamodel
# declaring them here allows them to be reused elsewhere
####
# The range must be one of:
# * A ClassDefinition, when the value of the slot is a complex object
# * A TypeDefinition, when the value of the slot is an atomic object
# * An EnumDefinition, when the value of the slot is a token that represents a vocabulary element
# * A boolean combination of the above
slots:
  id:
    identifier: true # unique key for a person
  full_name: 
    required: true # must be supplied
    description:
      name of the person
    slot_uri: schema:name
    ifabsent: string(Max Mustermann) # set a default value
  aliases:
    multivalued: true # range is a list
    description:
      other names for the person
  phone:
    pattern: "^[\\d\\(\\)\\-]+$" # regular expression
    slot_uri: schema:telephone 
  age:
    range: integer # an int between 0 and 200
    minimum_value: 0
    maximum_value: 200
  status:
    description: >-
      vital status of the person
    range: PersonStatus

enums:
  PersonStatus:
    permissible_values:
      ALIVE:
        description: the person is living
        meaning: PATO:0001421
      DEAD:
        description: the person is deceased
        meaning: PATO:0001422
      UNKNOWN:
        description: the vital status is not known
        todos:
          - map this to an ontology
```



















## YAML Files Example

### person_info.yaml

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:                                  ## Note are adding 3 new ones here
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  personinfo: https://w3id.org/linkml/examples/personinfo/
  ORCID: https://orcid.org/
imports:
  - linkml:types
default_range: string

classes:
  Person:
    class_uri: schema:Person              ## reuse schema.org vocabulary
    attributes:
      id:
        identifier: true
      full_name:
        required: true
        description:
          name of the person
        slot_uri: schema:name             ## reuse schema.org vocabulary
      aliases:
        multivalued: true
        description:
          other names for the person
      phone:
        pattern: "^[\\d\\(\\)\\-]+$"
        slot_uri: schema:telephone       ## reuse schema.org vocabulary
      age:
        range: integer
        minimum_value: 0
        maximum_value: 200
    id_prefixes:
      - ORCID
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person
```

### data.yaml

```yaml
persons:
  - id: ORCID:1234
    full_name: Clark Kent
    age: 33
    phone: 555-555-5555
  - id: ORCID:4567
    full_name: Lois Lane
    age: 34
```

## Convert to JSON

`gen-json-schema yaml/personinfo.yaml > json/personinfo.json`

## Validating Data

**Good Input:** `linkml-validate -s personinfo.yaml data.yaml`
- Output: `No issues found`

**Bad Input:** `linkml-validate -s personinfo.yaml bad_data.yaml`
- Output: `[ERROR] [yaml/bad_data.yaml/0] Additional properties are not allowed ('age', 'full_name', 'id', 'made_up_field', 'phone' were unexpected) in /`

## Converting to RDF

`linkml-convert -s yaml/personinfo.yaml yaml/data.yaml -o ttl/person.ttl`

