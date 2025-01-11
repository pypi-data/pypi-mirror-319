# GetMessagingActionResponseEmbedded

The embedded response associated with the messaging action.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_schema** | [**GetSchemaResponse**](GetSchemaResponse.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.get_messaging_action_response_embedded import GetMessagingActionResponseEmbedded

# TODO update the JSON string below
json = "{}"
# create an instance of GetMessagingActionResponseEmbedded from a JSON string
get_messaging_action_response_embedded_instance = GetMessagingActionResponseEmbedded.from_json(json)
# print the JSON string representation of the object
print(GetMessagingActionResponseEmbedded.to_json())

# convert the object into a dict
get_messaging_action_response_embedded_dict = get_messaging_action_response_embedded_instance.to_dict()
# create an instance of GetMessagingActionResponseEmbedded from a dict
get_messaging_action_response_embedded_from_dict = GetMessagingActionResponseEmbedded.from_dict(get_messaging_action_response_embedded_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


