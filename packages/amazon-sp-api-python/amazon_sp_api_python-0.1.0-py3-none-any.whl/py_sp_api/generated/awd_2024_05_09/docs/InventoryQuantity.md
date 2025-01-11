# InventoryQuantity

Quantity of inventory with an associated measurement unit context.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**quantity** | **float** | Quantity of the respective inventory. | 
**unit_of_measurement** | [**InventoryUnitOfMeasurement**](InventoryUnitOfMeasurement.md) |  | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inventory_quantity import InventoryQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of InventoryQuantity from a JSON string
inventory_quantity_instance = InventoryQuantity.from_json(json)
# print the JSON string representation of the object
print(InventoryQuantity.to_json())

# convert the object into a dict
inventory_quantity_dict = inventory_quantity_instance.to_dict()
# create an instance of InventoryQuantity from a dict
inventory_quantity_from_dict = InventoryQuantity.from_dict(inventory_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


