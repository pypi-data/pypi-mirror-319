# GetSolicitationActionsForOrderResponseLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_self** | [**LinkObject**](LinkObject.md) |  | 
**actions** | [**List[LinkObject]**](LinkObject.md) | Eligible actions for the specified amazonOrderId. | 

## Example

```python
from py_sp_api.generated.solicitations.models.get_solicitation_actions_for_order_response_links import GetSolicitationActionsForOrderResponseLinks

# TODO update the JSON string below
json = "{}"
# create an instance of GetSolicitationActionsForOrderResponseLinks from a JSON string
get_solicitation_actions_for_order_response_links_instance = GetSolicitationActionsForOrderResponseLinks.from_json(json)
# print the JSON string representation of the object
print(GetSolicitationActionsForOrderResponseLinks.to_json())

# convert the object into a dict
get_solicitation_actions_for_order_response_links_dict = get_solicitation_actions_for_order_response_links_instance.to_dict()
# create an instance of GetSolicitationActionsForOrderResponseLinks from a dict
get_solicitation_actions_for_order_response_links_from_dict = GetSolicitationActionsForOrderResponseLinks.from_dict(get_solicitation_actions_for_order_response_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


