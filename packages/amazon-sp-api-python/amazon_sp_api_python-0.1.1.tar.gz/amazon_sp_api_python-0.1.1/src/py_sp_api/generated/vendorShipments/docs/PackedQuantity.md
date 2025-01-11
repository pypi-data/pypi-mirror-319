# PackedQuantity

Details of item quantity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **int** | Amount of units shipped for a specific item at a shipment level. If the item is present only in certain cartons or pallets within the shipment, please provide this at the appropriate carton or pallet level. | 
**unit_of_measure** | **str** | Unit of measure for the shipped quantity. | 
**unit_size** | **int** | The case size, in the event that we ordered using cases. Otherwise, 1. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.packed_quantity import PackedQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of PackedQuantity from a JSON string
packed_quantity_instance = PackedQuantity.from_json(json)
# print the JSON string representation of the object
print(PackedQuantity.to_json())

# convert the object into a dict
packed_quantity_dict = packed_quantity_instance.to_dict()
# create an instance of PackedQuantity from a dict
packed_quantity_from_dict = PackedQuantity.from_dict(packed_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


