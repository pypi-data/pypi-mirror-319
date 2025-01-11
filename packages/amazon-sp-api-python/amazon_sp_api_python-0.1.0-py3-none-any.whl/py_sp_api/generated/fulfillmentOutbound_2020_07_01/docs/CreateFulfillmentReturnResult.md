# CreateFulfillmentReturnResult

The result for the createFulfillmentReturn operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**return_items** | [**List[ReturnItem]**](ReturnItem.md) | An array of items that Amazon accepted for return. Returns empty if no items were accepted for return. | [optional] 
**invalid_return_items** | [**List[InvalidReturnItem]**](InvalidReturnItem.md) | An array of invalid return item information. | [optional] 
**return_authorizations** | [**List[ReturnAuthorization]**](ReturnAuthorization.md) | An array of return authorization information. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.create_fulfillment_return_result import CreateFulfillmentReturnResult

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFulfillmentReturnResult from a JSON string
create_fulfillment_return_result_instance = CreateFulfillmentReturnResult.from_json(json)
# print the JSON string representation of the object
print(CreateFulfillmentReturnResult.to_json())

# convert the object into a dict
create_fulfillment_return_result_dict = create_fulfillment_return_result_instance.to_dict()
# create an instance of CreateFulfillmentReturnResult from a dict
create_fulfillment_return_result_from_dict = CreateFulfillmentReturnResult.from_dict(create_fulfillment_return_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


