# OperationProblem

A problem with additional properties persisted to an operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | An error code that identifies the type of error that occurred. | 
**details** | **str** | Additional details that can help the caller understand or fix the issue. | [optional] 
**message** | **str** | A message that describes the error condition. | 
**severity** | **str** | The severity of the problem. Possible values: &#x60;WARNING&#x60;, &#x60;ERROR&#x60;. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.operation_problem import OperationProblem

# TODO update the JSON string below
json = "{}"
# create an instance of OperationProblem from a JSON string
operation_problem_instance = OperationProblem.from_json(json)
# print the JSON string representation of the object
print(OperationProblem.to_json())

# convert the object into a dict
operation_problem_dict = operation_problem_instance.to_dict()
# create an instance of OperationProblem from a dict
operation_problem_from_dict = OperationProblem.from_dict(operation_problem_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


