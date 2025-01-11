# IntegerWithUnits

A whole number dimension and its unit of measurement. For example, this can represent 100 pixels.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **int** | The dimension value. | 
**units** | **str** | The unit of measurement. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.integer_with_units import IntegerWithUnits

# TODO update the JSON string below
json = "{}"
# create an instance of IntegerWithUnits from a JSON string
integer_with_units_instance = IntegerWithUnits.from_json(json)
# print the JSON string representation of the object
print(IntegerWithUnits.to_json())

# convert the object into a dict
integer_with_units_dict = integer_with_units_instance.to_dict()
# create an instance of IntegerWithUnits from a dict
integer_with_units_from_dict = IntegerWithUnits.from_dict(integer_with_units_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


