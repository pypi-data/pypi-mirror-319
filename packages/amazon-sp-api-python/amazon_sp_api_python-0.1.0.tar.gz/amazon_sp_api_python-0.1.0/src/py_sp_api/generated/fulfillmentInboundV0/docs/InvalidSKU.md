# InvalidSKU

Contains detail about an invalid SKU

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | [optional] 
**error_reason** | [**ErrorReason**](ErrorReason.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.invalid_sku import InvalidSKU

# TODO update the JSON string below
json = "{}"
# create an instance of InvalidSKU from a JSON string
invalid_sku_instance = InvalidSKU.from_json(json)
# print the JSON string representation of the object
print(InvalidSKU.to_json())

# convert the object into a dict
invalid_sku_dict = invalid_sku_instance.to_dict()
# create an instance of InvalidSKU from a dict
invalid_sku_from_dict = InvalidSKU.from_dict(invalid_sku_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


