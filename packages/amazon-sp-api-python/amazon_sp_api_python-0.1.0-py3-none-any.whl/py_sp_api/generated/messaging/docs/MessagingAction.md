# MessagingAction

A simple object containing the name of the template.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the template. | 

## Example

```python
from py_sp_api.generated.messaging.models.messaging_action import MessagingAction

# TODO update the JSON string below
json = "{}"
# create an instance of MessagingAction from a JSON string
messaging_action_instance = MessagingAction.from_json(json)
# print the JSON string representation of the object
print(MessagingAction.to_json())

# convert the object into a dict
messaging_action_dict = messaging_action_instance.to_dict()
# create an instance of MessagingAction from a dict
messaging_action_from_dict = MessagingAction.from_dict(messaging_action_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


