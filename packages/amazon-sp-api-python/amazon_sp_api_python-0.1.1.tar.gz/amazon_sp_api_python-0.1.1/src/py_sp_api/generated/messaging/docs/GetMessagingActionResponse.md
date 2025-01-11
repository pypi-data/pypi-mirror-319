# GetMessagingActionResponse

Describes a messaging action that can be taken for an order. Provides a JSON Hypertext Application Language (HAL) link to the JSON schema document that describes the expected input.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**links** | [**GetMessagingActionResponseLinks**](GetMessagingActionResponseLinks.md) |  | [optional] 
**embedded** | [**GetMessagingActionResponseEmbedded**](GetMessagingActionResponseEmbedded.md) |  | [optional] 
**payload** | [**MessagingAction**](MessagingAction.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.get_messaging_action_response import GetMessagingActionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetMessagingActionResponse from a JSON string
get_messaging_action_response_instance = GetMessagingActionResponse.from_json(json)
# print the JSON string representation of the object
print(GetMessagingActionResponse.to_json())

# convert the object into a dict
get_messaging_action_response_dict = get_messaging_action_response_instance.to_dict()
# create an instance of GetMessagingActionResponse from a dict
get_messaging_action_response_from_dict = GetMessagingActionResponse.from_dict(get_messaging_action_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


