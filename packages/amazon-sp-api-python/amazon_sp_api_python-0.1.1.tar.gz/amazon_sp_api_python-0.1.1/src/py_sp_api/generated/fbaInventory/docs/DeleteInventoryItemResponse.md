# DeleteInventoryItemResponse

The response schema for the DeleteInventoryItem operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.delete_inventory_item_response import DeleteInventoryItemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteInventoryItemResponse from a JSON string
delete_inventory_item_response_instance = DeleteInventoryItemResponse.from_json(json)
# print the JSON string representation of the object
print(DeleteInventoryItemResponse.to_json())

# convert the object into a dict
delete_inventory_item_response_dict = delete_inventory_item_response_instance.to_dict()
# create an instance of DeleteInventoryItemResponse from a dict
delete_inventory_item_response_from_dict = DeleteInventoryItemResponse.from_dict(delete_inventory_item_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


