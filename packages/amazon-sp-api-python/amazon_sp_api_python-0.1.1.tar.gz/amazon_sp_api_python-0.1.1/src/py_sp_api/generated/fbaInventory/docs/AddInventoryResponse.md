# AddInventoryResponse

The response schema for the AddInventory operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.add_inventory_response import AddInventoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AddInventoryResponse from a JSON string
add_inventory_response_instance = AddInventoryResponse.from_json(json)
# print the JSON string representation of the object
print(AddInventoryResponse.to_json())

# convert the object into a dict
add_inventory_response_dict = add_inventory_response_instance.to_dict()
# create an instance of AddInventoryResponse from a dict
add_inventory_response_from_dict = AddInventoryResponse.from_dict(add_inventory_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


