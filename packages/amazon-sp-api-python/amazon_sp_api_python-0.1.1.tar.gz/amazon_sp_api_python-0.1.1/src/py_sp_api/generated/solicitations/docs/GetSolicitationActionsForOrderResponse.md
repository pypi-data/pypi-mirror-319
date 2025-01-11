# GetSolicitationActionsForOrderResponse

The response schema for the getSolicitationActionsForOrder operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**links** | [**GetSolicitationActionsForOrderResponseLinks**](GetSolicitationActionsForOrderResponseLinks.md) |  | [optional] 
**embedded** | [**GetSolicitationActionsForOrderResponseEmbedded**](GetSolicitationActionsForOrderResponseEmbedded.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.solicitations.models.get_solicitation_actions_for_order_response import GetSolicitationActionsForOrderResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSolicitationActionsForOrderResponse from a JSON string
get_solicitation_actions_for_order_response_instance = GetSolicitationActionsForOrderResponse.from_json(json)
# print the JSON string representation of the object
print(GetSolicitationActionsForOrderResponse.to_json())

# convert the object into a dict
get_solicitation_actions_for_order_response_dict = get_solicitation_actions_for_order_response_instance.to_dict()
# create an instance of GetSolicitationActionsForOrderResponse from a dict
get_solicitation_actions_for_order_response_from_dict = GetSolicitationActionsForOrderResponse.from_dict(get_solicitation_actions_for_order_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


