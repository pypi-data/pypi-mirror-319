# RecordActionFeedbackRequest

The request for the `recordActionFeedback` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feedback_action_code** | **str** | The unique identifier for each notification status. | 

## Example

```python
from py_sp_api.generated.appIntegrations_2024_04_01.models.record_action_feedback_request import RecordActionFeedbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RecordActionFeedbackRequest from a JSON string
record_action_feedback_request_instance = RecordActionFeedbackRequest.from_json(json)
# print the JSON string representation of the object
print(RecordActionFeedbackRequest.to_json())

# convert the object into a dict
record_action_feedback_request_dict = record_action_feedback_request_instance.to_dict()
# create an instance of RecordActionFeedbackRequest from a dict
record_action_feedback_request_from_dict = RecordActionFeedbackRequest.from_dict(record_action_feedback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


