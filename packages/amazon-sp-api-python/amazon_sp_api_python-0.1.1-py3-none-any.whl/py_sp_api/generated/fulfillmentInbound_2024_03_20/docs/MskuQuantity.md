# MskuQuantity

Represents an MSKU and the related quantity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**msku** | **str** | The merchant SKU, a merchant-supplied identifier for a specific SKU. | 
**quantity** | **int** | A positive integer. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.msku_quantity import MskuQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of MskuQuantity from a JSON string
msku_quantity_instance = MskuQuantity.from_json(json)
# print the JSON string representation of the object
print(MskuQuantity.to_json())

# convert the object into a dict
msku_quantity_dict = msku_quantity_instance.to_dict()
# create an instance of MskuQuantity from a dict
msku_quantity_from_dict = MskuQuantity.from_dict(msku_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


