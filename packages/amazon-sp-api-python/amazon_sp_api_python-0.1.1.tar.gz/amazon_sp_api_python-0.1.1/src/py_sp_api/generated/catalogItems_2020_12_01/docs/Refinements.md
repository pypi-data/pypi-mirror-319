# Refinements

Search refinements.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**brands** | [**List[BrandRefinement]**](BrandRefinement.md) | Brand search refinements. | 
**classifications** | [**List[ClassificationRefinement]**](ClassificationRefinement.md) | Classification search refinements. | 

## Example

```python
from py_sp_api.generated.catalogItems_2020_12_01.models.refinements import Refinements

# TODO update the JSON string below
json = "{}"
# create an instance of Refinements from a JSON string
refinements_instance = Refinements.from_json(json)
# print the JSON string representation of the object
print(Refinements.to_json())

# convert the object into a dict
refinements_dict = refinements_instance.to_dict()
# create an instance of Refinements from a dict
refinements_from_dict = Refinements.from_dict(refinements_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


