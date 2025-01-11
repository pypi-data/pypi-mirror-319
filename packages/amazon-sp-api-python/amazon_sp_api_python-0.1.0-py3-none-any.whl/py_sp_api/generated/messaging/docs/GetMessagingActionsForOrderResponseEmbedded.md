# GetMessagingActionsForOrderResponseEmbedded

The messaging actions response that is associated with the specified `amazonOrderId`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**actions** | [**List[GetMessagingActionResponse]**](GetMessagingActionResponse.md) |  | 

## Example

```python
from py_sp_api.generated.messaging.models.get_messaging_actions_for_order_response_embedded import GetMessagingActionsForOrderResponseEmbedded

# TODO update the JSON string below
json = "{}"
# create an instance of GetMessagingActionsForOrderResponseEmbedded from a JSON string
get_messaging_actions_for_order_response_embedded_instance = GetMessagingActionsForOrderResponseEmbedded.from_json(json)
# print the JSON string representation of the object
print(GetMessagingActionsForOrderResponseEmbedded.to_json())

# convert the object into a dict
get_messaging_actions_for_order_response_embedded_dict = get_messaging_actions_for_order_response_embedded_instance.to_dict()
# create an instance of GetMessagingActionsForOrderResponseEmbedded from a dict
get_messaging_actions_for_order_response_embedded_from_dict = GetMessagingActionsForOrderResponseEmbedded.from_dict(get_messaging_actions_for_order_response_embedded_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


