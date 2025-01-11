# ItemQuantity

Details of quantity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **int** | Quantity of an item. This value should not be zero. | 
**unit_of_measure** | **str** | Unit of measure for the quantity. | 
**unit_size** | **int** | The case size, if the unit of measure value is Cases. | [optional] 
**total_weight** | [**TotalWeight**](TotalWeight.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.item_quantity import ItemQuantity

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


