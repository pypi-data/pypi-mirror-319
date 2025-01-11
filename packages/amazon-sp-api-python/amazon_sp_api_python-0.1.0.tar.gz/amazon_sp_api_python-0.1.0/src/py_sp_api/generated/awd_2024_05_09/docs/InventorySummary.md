# InventorySummary

Summary of inventory per SKU.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expiration_details** | [**List[ExpirationDetails]**](ExpirationDetails.md) | The expiration details of the inventory. This object will only appear if the &#x60;details&#x60; parameter in the request is set to &#x60;SHOW&#x60;. | [optional] 
**inventory_details** | [**InventoryDetails**](InventoryDetails.md) |  | [optional] 
**sku** | **str** | The seller or merchant SKU. | 
**total_inbound_quantity** | **int** | Total quantity that is in-transit from the seller and has not yet been received at an AWD Distribution Center | [optional] 
**total_onhand_quantity** | **int** | Total quantity that is present in AWD distribution centers. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inventory_summary import InventorySummary

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


