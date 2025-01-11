# InventoryUpdate

Inventory details required to update some or all items for the requested warehouse.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**is_full_update** | **bool** | When true, this request contains a full feed. Otherwise, this request contains a partial feed. When sending a full feed, you must send information about all items in the warehouse. Any items not in the full feed are updated as not available. When sending a partial feed, only include the items that need an update to inventory. The status of other items will remain unchanged. | 
**items** | [**List[ItemDetails]**](ItemDetails.md) | A list of inventory items with updated details, including quantity available. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentInventoryV1.models.inventory_update import InventoryUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of InventoryUpdate from a JSON string
inventory_update_instance = InventoryUpdate.from_json(json)
# print the JSON string representation of the object
print(InventoryUpdate.to_json())

# convert the object into a dict
inventory_update_dict = inventory_update_instance.to_dict()
# create an instance of InventoryUpdate from a dict
inventory_update_from_dict = InventoryUpdate.from_dict(inventory_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


