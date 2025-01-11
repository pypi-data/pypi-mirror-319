# CreateFulfillmentReturnResponse

The response schema for the `createFulfillmentReturn` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CreateFulfillmentReturnResult**](CreateFulfillmentReturnResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.create_fulfillment_return_response import CreateFulfillmentReturnResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFulfillmentReturnResponse from a JSON string
create_fulfillment_return_response_instance = CreateFulfillmentReturnResponse.from_json(json)
# print the JSON string representation of the object
print(CreateFulfillmentReturnResponse.to_json())

# convert the object into a dict
create_fulfillment_return_response_dict = create_fulfillment_return_response_instance.to_dict()
# create an instance of CreateFulfillmentReturnResponse from a dict
create_fulfillment_return_response_from_dict = CreateFulfillmentReturnResponse.from_dict(create_fulfillment_return_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


