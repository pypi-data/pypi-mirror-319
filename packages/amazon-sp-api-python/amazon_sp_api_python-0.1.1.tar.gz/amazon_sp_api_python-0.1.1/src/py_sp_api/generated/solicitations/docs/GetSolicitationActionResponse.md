# GetSolicitationActionResponse

Describes a solicitation action that can be taken for an order. Provides a JSON Hypertext Application Language (HAL) link to the JSON schema document that describes the expected input.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**links** | [**GetSolicitationActionResponseLinks**](GetSolicitationActionResponseLinks.md) |  | [optional] 
**embedded** | [**GetSolicitationActionResponseEmbedded**](GetSolicitationActionResponseEmbedded.md) |  | [optional] 
**payload** | [**SolicitationsAction**](SolicitationsAction.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.solicitations.models.get_solicitation_action_response import GetSolicitationActionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSolicitationActionResponse from a JSON string
get_solicitation_action_response_instance = GetSolicitationActionResponse.from_json(json)
# print the JSON string representation of the object
print(GetSolicitationActionResponse.to_json())

# convert the object into a dict
get_solicitation_action_response_dict = get_solicitation_action_response_instance.to_dict()
# create an instance of GetSolicitationActionResponse from a dict
get_solicitation_action_response_from_dict = GetSolicitationActionResponse.from_dict(get_solicitation_action_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


