# CreateInventoryItemResponse

The response schema for the CreateInventoryItem operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.create_inventory_item_response import CreateInventoryItemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateInventoryItemResponse from a JSON string
create_inventory_item_response_instance = CreateInventoryItemResponse.from_json(json)
# print the JSON string representation of the object
print(CreateInventoryItemResponse.to_json())

# convert the object into a dict
create_inventory_item_response_dict = create_inventory_item_response_instance.to_dict()
# create an instance of CreateInventoryItemResponse from a dict
create_inventory_item_response_from_dict = CreateInventoryItemResponse.from_dict(create_inventory_item_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


