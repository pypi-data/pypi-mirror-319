# UpdateFulfillmentOrderResponse

The response schema for the `updateFulfillmentOrder` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.update_fulfillment_order_response import UpdateFulfillmentOrderResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateFulfillmentOrderResponse from a JSON string
update_fulfillment_order_response_instance = UpdateFulfillmentOrderResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateFulfillmentOrderResponse.to_json())

# convert the object into a dict
update_fulfillment_order_response_dict = update_fulfillment_order_response_instance.to_dict()
# create an instance of UpdateFulfillmentOrderResponse from a dict
update_fulfillment_order_response_from_dict = UpdateFulfillmentOrderResponse.from_dict(update_fulfillment_order_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


