# GetPrepInstructionsResponse

The response schema for the getPrepInstructions operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetPrepInstructionsResult**](GetPrepInstructionsResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_prep_instructions_response import GetPrepInstructionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPrepInstructionsResponse from a JSON string
get_prep_instructions_response_instance = GetPrepInstructionsResponse.from_json(json)
# print the JSON string representation of the object
print(GetPrepInstructionsResponse.to_json())

# convert the object into a dict
get_prep_instructions_response_dict = get_prep_instructions_response_instance.to_dict()
# create an instance of GetPrepInstructionsResponse from a dict
get_prep_instructions_response_from_dict = GetPrepInstructionsResponse.from_dict(get_prep_instructions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


