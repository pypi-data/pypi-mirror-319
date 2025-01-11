# DecimalWithUnits

The decimal value and unit.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **float** | The decimal value. | [optional] 
**units** | **str** | The unit of the decimal value. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.decimal_with_units import DecimalWithUnits

# TODO update the JSON string below
json = "{}"
# create an instance of DecimalWithUnits from a JSON string
decimal_with_units_instance = DecimalWithUnits.from_json(json)
# print the JSON string representation of the object
print(DecimalWithUnits.to_json())

# convert the object into a dict
decimal_with_units_dict = decimal_with_units_instance.to_dict()
# create an instance of DecimalWithUnits from a dict
decimal_with_units_from_dict = DecimalWithUnits.from_dict(decimal_with_units_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


