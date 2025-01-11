# CreateFulfillmentReturnRequest

The `createFulfillmentReturn` operation creates a fulfillment return for items that were fulfilled using the `createFulfillmentOrder` operation. For calls to `createFulfillmentReturn`, you must include `ReturnReasonCode` values returned by a previous call to the `listReturnReasonCodes` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[CreateReturnItem]**](CreateReturnItem.md) | An array of items to be returned. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.create_fulfillment_return_request import CreateFulfillmentReturnRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFulfillmentReturnRequest from a JSON string
create_fulfillment_return_request_instance = CreateFulfillmentReturnRequest.from_json(json)
# print the JSON string representation of the object
print(CreateFulfillmentReturnRequest.to_json())

# convert the object into a dict
create_fulfillment_return_request_dict = create_fulfillment_return_request_instance.to_dict()
# create an instance of CreateFulfillmentReturnRequest from a dict
create_fulfillment_return_request_from_dict = CreateFulfillmentReturnRequest.from_dict(create_fulfillment_return_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


