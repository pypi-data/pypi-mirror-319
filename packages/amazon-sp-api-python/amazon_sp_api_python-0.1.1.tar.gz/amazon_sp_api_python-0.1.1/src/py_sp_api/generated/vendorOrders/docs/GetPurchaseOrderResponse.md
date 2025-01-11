# GetPurchaseOrderResponse

The response schema for the getPurchaseOrder operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**Order**](Order.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.get_purchase_order_response import GetPurchaseOrderResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPurchaseOrderResponse from a JSON string
get_purchase_order_response_instance = GetPurchaseOrderResponse.from_json(json)
# print the JSON string representation of the object
print(GetPurchaseOrderResponse.to_json())

# convert the object into a dict
get_purchase_order_response_dict = get_purchase_order_response_instance.to_dict()
# create an instance of GetPurchaseOrderResponse from a dict
get_purchase_order_response_from_dict = GetPurchaseOrderResponse.from_dict(get_purchase_order_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


