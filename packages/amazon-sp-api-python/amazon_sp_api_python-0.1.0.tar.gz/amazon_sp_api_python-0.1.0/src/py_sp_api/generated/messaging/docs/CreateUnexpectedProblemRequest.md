# CreateUnexpectedProblemRequest

The request schema for the createUnexpectedProblem operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | The text to be sent to the buyer. Only links related to unexpected problem calls are allowed. Do not include HTML or email addresses. The text must be written in the buyer&#39;s language of preference, which can be retrieved from the GetAttributes operation. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_unexpected_problem_request import CreateUnexpectedProblemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUnexpectedProblemRequest from a JSON string
create_unexpected_problem_request_instance = CreateUnexpectedProblemRequest.from_json(json)
# print the JSON string representation of the object
print(CreateUnexpectedProblemRequest.to_json())

# convert the object into a dict
create_unexpected_problem_request_dict = create_unexpected_problem_request_instance.to_dict()
# create an instance of CreateUnexpectedProblemRequest from a dict
create_unexpected_problem_request_from_dict = CreateUnexpectedProblemRequest.from_dict(create_unexpected_problem_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


