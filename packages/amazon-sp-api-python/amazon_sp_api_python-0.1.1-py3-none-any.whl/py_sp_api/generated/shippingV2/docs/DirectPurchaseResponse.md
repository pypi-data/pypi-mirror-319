# DirectPurchaseResponse

The response schema for the directPurchaseShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**DirectPurchaseResult**](DirectPurchaseResult.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.direct_purchase_response import DirectPurchaseResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DirectPurchaseResponse from a JSON string
direct_purchase_response_instance = DirectPurchaseResponse.from_json(json)
# print the JSON string representation of the object
print(DirectPurchaseResponse.to_json())

# convert the object into a dict
direct_purchase_response_dict = direct_purchase_response_instance.to_dict()
# create an instance of DirectPurchaseResponse from a dict
direct_purchase_response_from_dict = DirectPurchaseResponse.from_dict(direct_purchase_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


