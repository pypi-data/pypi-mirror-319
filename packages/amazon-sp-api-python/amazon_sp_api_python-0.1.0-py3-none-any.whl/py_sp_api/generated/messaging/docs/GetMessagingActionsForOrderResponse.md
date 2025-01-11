# GetMessagingActionsForOrderResponse

The response schema for the `getMessagingActionsForOrder` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**links** | [**GetMessagingActionsForOrderResponseLinks**](GetMessagingActionsForOrderResponseLinks.md) |  | [optional] 
**embedded** | [**GetMessagingActionsForOrderResponseEmbedded**](GetMessagingActionsForOrderResponseEmbedded.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.get_messaging_actions_for_order_response import GetMessagingActionsForOrderResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetMessagingActionsForOrderResponse from a JSON string
get_messaging_actions_for_order_response_instance = GetMessagingActionsForOrderResponse.from_json(json)
# print the JSON string representation of the object
print(GetMessagingActionsForOrderResponse.to_json())

# convert the object into a dict
get_messaging_actions_for_order_response_dict = get_messaging_actions_for_order_response_instance.to_dict()
# create an instance of GetMessagingActionsForOrderResponse from a dict
get_messaging_actions_for_order_response_from_dict = GetMessagingActionsForOrderResponse.from_dict(get_messaging_actions_for_order_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


