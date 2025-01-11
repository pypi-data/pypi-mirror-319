# CreateNegativeFeedbackRemovalResponse

The response schema for the createNegativeFeedbackRemoval operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_negative_feedback_removal_response import CreateNegativeFeedbackRemovalResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateNegativeFeedbackRemovalResponse from a JSON string
create_negative_feedback_removal_response_instance = CreateNegativeFeedbackRemovalResponse.from_json(json)
# print the JSON string representation of the object
print(CreateNegativeFeedbackRemovalResponse.to_json())

# convert the object into a dict
create_negative_feedback_removal_response_dict = create_negative_feedback_removal_response_instance.to_dict()
# create an instance of CreateNegativeFeedbackRemovalResponse from a dict
create_negative_feedback_removal_response_from_dict = CreateNegativeFeedbackRemovalResponse.from_dict(create_negative_feedback_removal_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


