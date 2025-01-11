# GetMessagingActionResponseLinks

The links response that is associated with the messaging action.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_self** | [**LinkObject**](LinkObject.md) |  | 
**var_schema** | [**LinkObject**](LinkObject.md) |  | 

## Example

```python
from py_sp_api.generated.messaging.models.get_messaging_action_response_links import GetMessagingActionResponseLinks

# TODO update the JSON string below
json = "{}"
# create an instance of GetMessagingActionResponseLinks from a JSON string
get_messaging_action_response_links_instance = GetMessagingActionResponseLinks.from_json(json)
# print the JSON string representation of the object
print(GetMessagingActionResponseLinks.to_json())

# convert the object into a dict
get_messaging_action_response_links_dict = get_messaging_action_response_links_instance.to_dict()
# create an instance of GetMessagingActionResponseLinks from a dict
get_messaging_action_response_links_from_dict = GetMessagingActionResponseLinks.from_dict(get_messaging_action_response_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


