from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel
import sys
import inspect
import re
import json


class Overlay(BaseModel):
    capture_base: str = "00000000000000"
    type: str = "spec/overlays/overlay_type/1.0"
    language: str = "en"


"""
Optional is a bit misleading here. 
What it means technically means is that default_character_encoding 
can be a default_character_encoding or None, but it is still a required argument. 
To make it truly optional (as in, it doesn't have to be provided), 
you must provide a default --> None
"""

#####################
# Pragmatic - Context
#####################


class PragmaticAttributeMappingOverlay(Overlay):
    """An Attribute Mapping Overlay defines attribute mappings between two distinct data models. 
    Data mapping provides a preliminary step for data integration tasks, 
    including data transformation or data mediation between a data source and 
    a destination or consolidation of multiple databases into a single database and 
    identifying redundant columns of data for consolidation or elimination.

    Args (example):
        "first_name" : "firstName"
        "last_name":"surname"
    """
    attribute_mapping: Optional[dict] = None


class PragmaticUnitMappingOverlay(Overlay):
    """
    A Unit Mapping Overlay defines target units for quantitative data when 
    converting between different units of measurement.
    The attr_units attribute maps key-value pairs where the 
    key is the attribute name and the value is the desired unit of measurement.

    Args (example):
        "blood_glucose":"mg/dL"
    """
    attribute_units: Optional[dict] = None


class PragmaticUsageOverlay(Overlay):
    pass


class PragmaticConformanceOverlay(Overlay):
    pass


class PragmaticInformationOverlay(Overlay):
    attribute_information: Optional[dict] = None

#########################
# Semantic - Definitional
#########################


class SemanticUnitOverlay(Overlay):
    pass


class SemanticLabelOverlay(Overlay):
    attribute_labels: Optional[dict] = None
    attribute_categories: Optional[list] = None
    category_labels: Optional[dict] = None


class SemanticMetadataOverlay(Overlay):
    pass


class SemanticStandardOverlay(Overlay):
    attr_standards: Optional[dict] = None

##########################
# Morphologic - Structural
##########################


class MorphologicEncodingOverlay(Overlay):
    default_character_encoding: Optional[str] = None
    attr_character_encoding: Optional[dict] = None


class MorphologicCardinalityOverlay(Overlay):
    pass


class MorphologicDimensionalityOverlay(Overlay):
    pass


class MorphologicSizeOverlay(Overlay):
    pass

##########################


def allClasses():
    classes = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            classes.append(name)

    pragmatic = []
    semantic = []
    morphologic = []
    for c in classes:
        splitter = re.split('(?<=.)(?=[A-Z])', c)
        if splitter[0] == 'Pragmatic':
            pragmatic.append(''.join(splitter))
        if splitter[0] == 'Semantic':
            semantic.append(''.join(splitter))
        if splitter[0] == 'Morphologic':
            morphologic.append(''.join(splitter))
    return pragmatic, semantic, morphologic


if __name__ == '__main__':
    external_data = {
        "capture_base": "sadsajdghsadsaas",
        "type": "spec/overlays/character_encoding/1.0",
        "language": "en"
    }

    # Instanciate
    semOverlay = SemanticLabelOverlay(**external_data)
    # print(semOverlay.model_fields)
    out_file = semOverlay.model_dump()

    json_object = json.dumps(out_file, indent=4)
 
    # Writing to sample.json
    with open("oca/overlays/overlays.json", "w") as outfile:
        outfile.write(json_object)
