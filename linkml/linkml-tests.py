from linkml.validator import validate

instance = {
    "id": "ORCID:1234",
    "full_name": "Clark Kent",
    "age": 32,
    "phone": "555-555-5555",
    "test": "asdksjdskd"
}

report = validate(
    instance, "/Users/maximilianstaebler/code/SemanticDataLink/tutorials/linkml-tutorial/yaml/personinfo.yaml", "Person")

if not report.results:
    print('The instance is valid!')
else:
    for result in report.results:
        print(result.message)
