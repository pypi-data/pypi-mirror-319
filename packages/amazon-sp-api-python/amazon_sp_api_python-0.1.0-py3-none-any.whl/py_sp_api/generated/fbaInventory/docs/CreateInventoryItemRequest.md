# CreateInventoryItemRequest

An item to be created in the inventory.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | 
**marketplace_id** | **str** | The marketplaceId. | 
**product_name** | **str** | The name of the item. | 

## Example

```python
from py_sp_api.generated.fbaInventory.models.create_inventory_item_request import CreateInventoryItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateInventoryItemRequest from a JSON string
create_inventory_item_request_instance = CreateInventoryItemRequest.from_json(json)
# print the JSON string representation of the object
print(CreateInventoryItemRequest.to_json())

# convert the object into a dict
create_inventory_item_request_dict = create_inventory_item_request_instance.to_dict()
# create an instance of CreateInventoryItemRequest from a dict
create_inventory_item_request_from_dict = CreateInventoryItemRequest.from_dict(create_inventory_item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


