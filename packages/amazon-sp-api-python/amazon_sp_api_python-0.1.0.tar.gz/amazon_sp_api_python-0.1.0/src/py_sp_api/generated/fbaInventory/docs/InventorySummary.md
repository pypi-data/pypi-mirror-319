# InventorySummary

Inventory summary for a specific item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of an item. | [optional] 
**fn_sku** | **str** | Amazon&#39;s fulfillment network SKU identifier. | [optional] 
**seller_sku** | **str** | The seller SKU of the item. | [optional] 
**condition** | **str** | The condition of the item as described by the seller (for example, New Item). | [optional] 
**inventory_details** | [**InventoryDetails**](InventoryDetails.md) |  | [optional] 
**last_updated_time** | **datetime** | The date and time that any quantity was last updated. | [optional] 
**product_name** | **str** | The localized language product title of the item within the specific marketplace. | [optional] 
**total_quantity** | **int** | The total number of units in an inbound shipment or in Amazon fulfillment centers. | [optional] 
**stores** | **List[str]** | A list of seller-enrolled stores that apply to this seller SKU. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.inventory_summary import InventorySummary

# TODO update the JSON string below
json = "{}"
# create an instance of InventorySummary from a JSON string
inventory_summary_instance = InventorySummary.from_json(json)
# print the JSON string representation of the object
print(InventorySummary.to_json())

# convert the object into a dict
inventory_summary_dict = inventory_summary_instance.to_dict()
# create an instance of InventorySummary from a dict
inventory_summary_from_dict = InventorySummary.from_dict(inventory_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


