# Dimensions

Dimensions of an Amazon catalog item or item in its packaging.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**height** | [**Dimension**](Dimension.md) |  | [optional] 
**length** | [**Dimension**](Dimension.md) |  | [optional] 
**weight** | [**Dimension**](Dimension.md) |  | [optional] 
**width** | [**Dimension**](Dimension.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.dimensions import Dimensions

# TODO update the JSON string below
json = "{}"
# create an instance of Dimensions from a JSON string
dimensions_instance = Dimensions.from_json(json)
# print the JSON string representation of the object
print(Dimensions.to_json())

# convert the object into a dict
dimensions_dict = dimensions_instance.to_dict()
# create an instance of Dimensions from a dict
dimensions_from_dict = Dimensions.from_dict(dimensions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


