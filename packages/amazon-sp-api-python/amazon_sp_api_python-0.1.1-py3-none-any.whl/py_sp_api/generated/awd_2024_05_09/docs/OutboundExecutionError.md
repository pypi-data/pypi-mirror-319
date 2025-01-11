# OutboundExecutionError

Execution errors associated with the outbound order. This field will be populated if the order failed validation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**failure_code** | **str** | Failure code details for the error. | 
**failure_reasons** | **List[str]** | Failure reasons for the error. | 
**sku** | **str** | MSKU associated with the error. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.outbound_execution_error import OutboundExecutionError

# TODO update the JSON string below
json = "{}"
# create an instance of OutboundExecutionError from a JSON string
outbound_execution_error_instance = OutboundExecutionError.from_json(json)
# print the JSON string representation of the object
print(OutboundExecutionError.to_json())

# convert the object into a dict
outbound_execution_error_dict = outbound_execution_error_instance.to_dict()
# create an instance of OutboundExecutionError from a dict
outbound_execution_error_from_dict = OutboundExecutionError.from_dict(outbound_execution_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


