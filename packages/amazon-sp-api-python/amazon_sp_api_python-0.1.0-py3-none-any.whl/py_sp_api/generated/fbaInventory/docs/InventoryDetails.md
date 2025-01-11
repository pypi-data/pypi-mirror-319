# InventoryDetails

Summarized inventory details. This object will not appear if the details parameter in the request is false.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillable_quantity** | **int** | The item quantity that can be picked, packed, and shipped. | [optional] 
**inbound_working_quantity** | **int** | The number of units in an inbound shipment for which you have notified Amazon. | [optional] 
**inbound_shipped_quantity** | **int** | The number of units in an inbound shipment that you have notified Amazon about and have provided a tracking number. | [optional] 
**inbound_receiving_quantity** | **int** | The number of units that have not yet been received at an Amazon fulfillment center for processing, but are part of an inbound shipment with some units that have already been received and processed. | [optional] 
**reserved_quantity** | [**ReservedQuantity**](ReservedQuantity.md) |  | [optional] 
**researching_quantity** | [**ResearchingQuantity**](ResearchingQuantity.md) |  | [optional] 
**unfulfillable_quantity** | [**UnfulfillableQuantity**](UnfulfillableQuantity.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.inventory_details import InventoryDetails

# TODO update the JSON string below
json = "{}"
# create an instance of InventoryDetails from a JSON string
inventory_details_instance = InventoryDetails.from_json(json)
# print the JSON string representation of the object
print(InventoryDetails.to_json())

# convert the object into a dict
inventory_details_dict = inventory_details_instance.to_dict()
# create an instance of InventoryDetails from a dict
inventory_details_from_dict = InventoryDetails.from_dict(inventory_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


