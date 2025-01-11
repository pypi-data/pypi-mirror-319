# ItemQuantity

Details of item quantity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **int** | Quantity of units shipped for a specific item at a shipment level. If the item is present only in certain packages or pallets within the shipment, please provide this at the appropriate package or pallet level. | 
**unit_of_measure** | **str** | Unit of measure for the shipped quantity. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.item_quantity import ItemQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of ItemQuantity from a JSON string
item_quantity_instance = ItemQuantity.from_json(json)
# print the JSON string representation of the object
print(ItemQuantity.to_json())

# convert the object into a dict
item_quantity_dict = item_quantity_instance.to_dict()
# create an instance of ItemQuantity from a dict
item_quantity_from_dict = ItemQuantity.from_dict(item_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


