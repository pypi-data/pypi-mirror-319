# SubmitFulfillmentOrderStatusUpdateResponse

The response schema for the `SubmitFulfillmentOrderStatusUpdate` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.submit_fulfillment_order_status_update_response import SubmitFulfillmentOrderStatusUpdateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitFulfillmentOrderStatusUpdateResponse from a JSON string
submit_fulfillment_order_status_update_response_instance = SubmitFulfillmentOrderStatusUpdateResponse.from_json(json)
# print the JSON string representation of the object
print(SubmitFulfillmentOrderStatusUpdateResponse.to_json())

# convert the object into a dict
submit_fulfillment_order_status_update_response_dict = submit_fulfillment_order_status_update_response_instance.to_dict()
# create an instance of SubmitFulfillmentOrderStatusUpdateResponse from a dict
submit_fulfillment_order_status_update_response_from_dict = SubmitFulfillmentOrderStatusUpdateResponse.from_dict(submit_fulfillment_order_status_update_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


