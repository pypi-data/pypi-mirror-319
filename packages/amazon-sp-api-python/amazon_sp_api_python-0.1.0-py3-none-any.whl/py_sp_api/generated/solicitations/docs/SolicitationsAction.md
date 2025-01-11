# SolicitationsAction

A simple object containing the name of the template.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 

## Example

```python
from py_sp_api.generated.solicitations.models.solicitations_action import SolicitationsAction

# TODO update the JSON string below
json = "{}"
# create an instance of SolicitationsAction from a JSON string
solicitations_action_instance = SolicitationsAction.from_json(json)
# print the JSON string representation of the object
print(SolicitationsAction.to_json())

# convert the object into a dict
solicitations_action_dict = solicitations_action_instance.to_dict()
# create an instance of SolicitationsAction from a dict
solicitations_action_from_dict = SolicitationsAction.from_dict(solicitations_action_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


