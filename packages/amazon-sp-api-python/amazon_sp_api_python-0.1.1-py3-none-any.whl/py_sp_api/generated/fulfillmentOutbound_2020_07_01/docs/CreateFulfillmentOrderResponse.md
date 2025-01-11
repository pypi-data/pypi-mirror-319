# CreateFulfillmentOrderResponse

The response schema for the `createFulfillmentOrder` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.create_fulfillment_order_response import CreateFulfillmentOrderResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFulfillmentOrderResponse from a JSON string
create_fulfillment_order_response_instance = CreateFulfillmentOrderResponse.from_json(json)
# print the JSON string representation of the object
print(CreateFulfillmentOrderResponse.to_json())

# convert the object into a dict
create_fulfillment_order_response_dict = create_fulfillment_order_response_instance.to_dict()
# create an instance of CreateFulfillmentOrderResponse from a dict
create_fulfillment_order_response_from_dict = CreateFulfillmentOrderResponse.from_dict(create_fulfillment_order_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


