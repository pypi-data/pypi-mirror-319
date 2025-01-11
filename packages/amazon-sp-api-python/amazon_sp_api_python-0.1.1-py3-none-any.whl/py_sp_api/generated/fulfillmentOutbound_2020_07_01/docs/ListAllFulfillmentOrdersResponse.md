# ListAllFulfillmentOrdersResponse

The response schema for the `listAllFulfillmentOrders` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ListAllFulfillmentOrdersResult**](ListAllFulfillmentOrdersResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.list_all_fulfillment_orders_response import ListAllFulfillmentOrdersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListAllFulfillmentOrdersResponse from a JSON string
list_all_fulfillment_orders_response_instance = ListAllFulfillmentOrdersResponse.from_json(json)
# print the JSON string representation of the object
print(ListAllFulfillmentOrdersResponse.to_json())

# convert the object into a dict
list_all_fulfillment_orders_response_dict = list_all_fulfillment_orders_response_instance.to_dict()
# create an instance of ListAllFulfillmentOrdersResponse from a dict
list_all_fulfillment_orders_response_from_dict = ListAllFulfillmentOrdersResponse.from_dict(list_all_fulfillment_orders_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


