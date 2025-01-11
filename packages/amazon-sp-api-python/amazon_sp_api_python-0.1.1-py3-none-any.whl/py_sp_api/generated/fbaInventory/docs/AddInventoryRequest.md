# AddInventoryRequest

The object with the list of Inventory to be added

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inventory_items** | [**List[InventoryItem]**](InventoryItem.md) | List of Inventory to be added | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.add_inventory_request import AddInventoryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddInventoryRequest from a JSON string
add_inventory_request_instance = AddInventoryRequest.from_json(json)
# print the JSON string representation of the object
print(AddInventoryRequest.to_json())

# convert the object into a dict
add_inventory_request_dict = add_inventory_request_instance.to_dict()
# create an instance of AddInventoryRequest from a dict
add_inventory_request_from_dict = AddInventoryRequest.from_dict(add_inventory_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


