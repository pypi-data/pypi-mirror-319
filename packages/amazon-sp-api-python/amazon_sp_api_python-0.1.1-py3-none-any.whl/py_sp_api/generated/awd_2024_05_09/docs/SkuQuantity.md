# SkuQuantity

Quantity details for a SKU as part of a shipment

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expected_quantity** | [**InventoryQuantity**](InventoryQuantity.md) |  | 
**received_quantity** | [**InventoryQuantity**](InventoryQuantity.md) |  | [optional] 
**sku** | **str** | The merchant stock keeping unit | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.sku_quantity import SkuQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of SkuQuantity from a JSON string
sku_quantity_instance = SkuQuantity.from_json(json)
# print the JSON string representation of the object
print(SkuQuantity.to_json())

# convert the object into a dict
sku_quantity_dict = sku_quantity_instance.to_dict()
# create an instance of SkuQuantity from a dict
sku_quantity_from_dict = SkuQuantity.from_dict(sku_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


