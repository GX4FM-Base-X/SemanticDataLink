# LinkML

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

