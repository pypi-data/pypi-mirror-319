# CustomPlacementInput

Provide units going to the warehouse.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[ItemInput]**](ItemInput.md) | Items included while creating Inbound Plan. | 
**warehouse_id** | **str** | Warehouse Id. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.custom_placement_input import CustomPlacementInput

# TODO update the JSON string below
json = "{}"
# create an instance of CustomPlacementInput from a JSON string
custom_placement_input_instance = CustomPlacementInput.from_json(json)
# print the JSON string representation of the object
print(CustomPlacementInput.to_json())

# convert the object into a dict
custom_placement_input_dict = custom_placement_input_instance.to_dict()
# create an instance of CustomPlacementInput from a dict
custom_placement_input_from_dict = CustomPlacementInput.from_dict(custom_placement_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


