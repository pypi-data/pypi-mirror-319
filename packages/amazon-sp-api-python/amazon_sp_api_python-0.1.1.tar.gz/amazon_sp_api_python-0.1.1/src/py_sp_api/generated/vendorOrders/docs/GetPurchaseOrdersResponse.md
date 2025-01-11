# GetPurchaseOrdersResponse

The response schema for the getPurchaseOrders operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**OrderList**](OrderList.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.get_purchase_orders_response import GetPurchaseOrdersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPurchaseOrdersResponse from a JSON string
get_purchase_orders_response_instance = GetPurchaseOrdersResponse.from_json(json)
# print the JSON string representation of the object
print(GetPurchaseOrdersResponse.to_json())

# convert the object into a dict
get_purchase_orders_response_dict = get_purchase_orders_response_instance.to_dict()
# create an instance of GetPurchaseOrdersResponse from a dict
get_purchase_orders_response_from_dict = GetPurchaseOrdersResponse.from_dict(get_purchase_orders_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


