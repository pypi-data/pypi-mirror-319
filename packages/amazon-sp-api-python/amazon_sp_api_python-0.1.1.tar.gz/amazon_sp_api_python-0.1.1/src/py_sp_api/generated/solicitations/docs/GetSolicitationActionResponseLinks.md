# GetSolicitationActionResponseLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_self** | [**LinkObject**](LinkObject.md) |  | 
**var_schema** | [**LinkObject**](LinkObject.md) |  | 

## Example

```python
from py_sp_api.generated.solicitations.models.get_solicitation_action_response_links import GetSolicitationActionResponseLinks

# TODO update the JSON string below
json = "{}"
# create an instance of GetSolicitationActionResponseLinks from a JSON string
get_solicitation_action_response_links_instance = GetSolicitationActionResponseLinks.from_json(json)
# print the JSON string representation of the object
print(GetSolicitationActionResponseLinks.to_json())

# convert the object into a dict
get_solicitation_action_response_links_dict = get_solicitation_action_response_links_instance.to_dict()
# create an instance of GetSolicitationActionResponseLinks from a dict
get_solicitation_action_response_links_from_dict = GetSolicitationActionResponseLinks.from_dict(get_solicitation_action_response_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


