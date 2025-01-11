# DimensionType

The dimension type attribute of an item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**height** | [**DecimalWithUnits**](DecimalWithUnits.md) |  | [optional] 
**length** | [**DecimalWithUnits**](DecimalWithUnits.md) |  | [optional] 
**width** | [**DecimalWithUnits**](DecimalWithUnits.md) |  | [optional] 
**weight** | [**DecimalWithUnits**](DecimalWithUnits.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.dimension_type import DimensionType

# TODO update the JSON string below
json = "{}"
# create an instance of DimensionType from a JSON string
dimension_type_instance = DimensionType.from_json(json)
# print the JSON string representation of the object
print(DimensionType.to_json())

# convert the object into a dict
dimension_type_dict = dimension_type_instance.to_dict()
# create an instance of DimensionType from a dict
dimension_type_from_dict = DimensionType.from_dict(dimension_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


