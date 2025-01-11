# ReservedQuantity

The quantity of reserved inventory.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_reserved_quantity** | **int** | The total number of units in Amazon&#39;s fulfillment network that are currently being picked, packed, and shipped; or are sidelined for measurement, sampling, or other internal processes. | [optional] 
**pending_customer_order_quantity** | **int** | The number of units reserved for customer orders. | [optional] 
**pending_transshipment_quantity** | **int** | The number of units being transferred from one fulfillment center to another. | [optional] 
**fc_processing_quantity** | **int** | The number of units that have been sidelined at the fulfillment center for additional processing. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.reserved_quantity import ReservedQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of ReservedQuantity from a JSON string
reserved_quantity_instance = ReservedQuantity.from_json(json)
# print the JSON string representation of the object
print(ReservedQuantity.to_json())

# convert the object into a dict
reserved_quantity_dict = reserved_quantity_instance.to_dict()
# create an instance of ReservedQuantity from a dict
reserved_quantity_from_dict = ReservedQuantity.from_dict(reserved_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


