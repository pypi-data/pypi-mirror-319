# ShipsFromType

The state and country from where the item is shipped.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**state** | **str** | The state from where the item is shipped. | [optional] 
**country** | **str** | The country from where the item is shipped. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.ships_from_type import ShipsFromType

# TODO update the JSON string below
json = "{}"
# create an instance of ShipsFromType from a JSON string
ships_from_type_instance = ShipsFromType.from_json(json)
# print the JSON string representation of the object
print(ShipsFromType.to_json())

# convert the object into a dict
ships_from_type_dict = ships_from_type_instance.to_dict()
# create an instance of ShipsFromType from a dict
ships_from_type_from_dict = ShipsFromType.from_dict(ships_from_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


