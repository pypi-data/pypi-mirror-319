# ListAllFulfillmentOrdersResult

The request for the listAllFulfillmentOrders operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_token** | **str** | When present and not empty, pass this string token in the next request to return the next response page. | [optional] 
**fulfillment_orders** | [**List[FulfillmentOrder]**](FulfillmentOrder.md) | An array of fulfillment order information. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.list_all_fulfillment_orders_result import ListAllFulfillmentOrdersResult

# TODO update the JSON string below
json = "{}"
# create an instance of ListAllFulfillmentOrdersResult from a JSON string
list_all_fulfillment_orders_result_instance = ListAllFulfillmentOrdersResult.from_json(json)
# print the JSON string representation of the object
print(ListAllFulfillmentOrdersResult.to_json())

# convert the object into a dict
list_all_fulfillment_orders_result_dict = list_all_fulfillment_orders_result_instance.to_dict()
# create an instance of ListAllFulfillmentOrdersResult from a dict
list_all_fulfillment_orders_result_from_dict = ListAllFulfillmentOrdersResult.from_dict(list_all_fulfillment_orders_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


