# PropertyGroup

A property group represents a logical grouping of schema properties that can be used for display or informational purposes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | The display label of the property group. | [optional] 
**description** | **str** | The description of the property group. | [optional] 
**property_names** | **List[str]** | The names of the schema properties for the property group. | [optional] 

## Example

```python
from py_sp_api.generated.definitionsProductTypes_2020_09_01.models.property_group import PropertyGroup

# TODO update the JSON string below
json = "{}"
# create an instance of PropertyGroup from a JSON string
property_group_instance = PropertyGroup.from_json(json)
# print the JSON string representation of the object
print(PropertyGroup.to_json())

# convert the object into a dict
property_group_dict = property_group_instance.to_dict()
# create an instance of PropertyGroup from a dict
property_group_from_dict = PropertyGroup.from_dict(property_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


