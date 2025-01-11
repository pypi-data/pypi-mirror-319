# CreateUnexpectedProblemResponse

The response schema for the createUnexpectedProblem operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_unexpected_problem_response import CreateUnexpectedProblemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUnexpectedProblemResponse from a JSON string
create_unexpected_problem_response_instance = CreateUnexpectedProblemResponse.from_json(json)
# print the JSON string representation of the object
print(CreateUnexpectedProblemResponse.to_json())

# convert the object into a dict
create_unexpected_problem_response_dict = create_unexpected_problem_response_instance.to_dict()
# create an instance of CreateUnexpectedProblemResponse from a dict
create_unexpected_problem_response_from_dict = CreateUnexpectedProblemResponse.from_dict(create_unexpected_problem_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


