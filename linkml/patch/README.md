# What is the purpose of this directory?

## Fixes / Updates from a forked repository
This directory contains patches for linkml that are documented [here](https://github.com/GX4FM-Base-X/semantic-road-damange-detection/blob/main/ontologies-shacl/LinkML/README.md).
The sqlalchemy patch is not applied here since SemanticDataLink relies on the structure.

In short: Some generators are patched. This patches should be removed once the forked repository is merged back into the linkml repository.

## Fix of SHACL-Generator to add the suffix "Shape" to the class
The shaclgen.py contains a fix that adds the suffix Shape to the class to prevent name clashes when generating OWL and shacl. @Paul Moosmann will check with Christoph if this fix should also be applied to the forked repository.

# Summary
- all python files are taken from the forked repository
- the shaclgen.py contains the "Shape" suffix fix in addition.