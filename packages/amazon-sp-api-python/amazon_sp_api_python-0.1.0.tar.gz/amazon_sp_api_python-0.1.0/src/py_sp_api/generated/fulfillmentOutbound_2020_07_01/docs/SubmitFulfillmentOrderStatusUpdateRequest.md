# SubmitFulfillmentOrderStatusUpdateRequest

The request body schema for the `submitFulfillmentOrderStatusUpdate` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_order_status** | [**FulfillmentOrderStatus**](FulfillmentOrderStatus.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.submit_fulfillment_order_status_update_request import SubmitFulfillmentOrderStatusUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitFulfillmentOrderStatusUpdateRequest from a JSON string
submit_fulfillment_order_status_update_request_instance = SubmitFulfillmentOrderStatusUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(SubmitFulfillmentOrderStatusUpdateRequest.to_json())

# convert the object into a dict
submit_fulfillment_order_status_update_request_dict = submit_fulfillment_order_status_update_request_instance.to_dict()
# create an instance of SubmitFulfillmentOrderStatusUpdateRequest from a dict
submit_fulfillment_order_status_update_request_from_dict = SubmitFulfillmentOrderStatusUpdateRequest.from_dict(submit_fulfillment_order_status_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


