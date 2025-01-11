# GetMessagingActionsForOrderResponseLinks

The links response that is associated with the specified `amazonOrderId`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_self** | [**LinkObject**](LinkObject.md) |  | 
**actions** | [**List[LinkObject]**](LinkObject.md) | Eligible actions for the specified amazonOrderId. | 

## Example

```python
from py_sp_api.generated.messaging.models.get_messaging_actions_for_order_response_links import GetMessagingActionsForOrderResponseLinks

# TODO update the JSON string below
json = "{}"
# create an instance of GetMessagingActionsForOrderResponseLinks from a JSON string
get_messaging_actions_for_order_response_links_instance = GetMessagingActionsForOrderResponseLinks.from_json(json)
# print the JSON string representation of the object
print(GetMessagingActionsForOrderResponseLinks.to_json())

# convert the object into a dict
get_messaging_actions_for_order_response_links_dict = get_messaging_actions_for_order_response_links_instance.to_dict()
# create an instance of GetMessagingActionsForOrderResponseLinks from a dict
get_messaging_actions_for_order_response_links_from_dict = GetMessagingActionsForOrderResponseLinks.from_dict(get_messaging_actions_for_order_response_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


