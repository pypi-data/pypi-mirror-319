# InboundOperationStatus

GetInboundOperationStatus response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation** | **str** | The name of the operation in the asynchronous API call. | 
**operation_id** | **str** | The operation ID returned by the asynchronous API call. | 
**operation_problems** | [**List[OperationProblem]**](OperationProblem.md) | The problems in the processing of the asynchronous operation. | 
**operation_status** | [**OperationStatus**](OperationStatus.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.inbound_operation_status import InboundOperationStatus

# TODO update the JSON string below
json = "{}"
# create an instance of InboundOperationStatus from a JSON string
inbound_operation_status_instance = InboundOperationStatus.from_json(json)
# print the JSON string representation of the object
print(InboundOperationStatus.to_json())

# convert the object into a dict
inbound_operation_status_dict = inbound_operation_status_instance.to_dict()
# create an instance of InboundOperationStatus from a dict
inbound_operation_status_from_dict = InboundOperationStatus.from_dict(inbound_operation_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


