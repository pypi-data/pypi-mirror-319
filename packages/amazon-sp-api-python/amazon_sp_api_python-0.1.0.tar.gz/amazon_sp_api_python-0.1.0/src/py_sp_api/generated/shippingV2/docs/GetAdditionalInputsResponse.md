# GetAdditionalInputsResponse

The response schema for the getAdditionalInputs operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | **Dict[str, object]** | The JSON schema to use to provide additional inputs when required to purchase a shipping offering. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_additional_inputs_response import GetAdditionalInputsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetAdditionalInputsResponse from a JSON string
get_additional_inputs_response_instance = GetAdditionalInputsResponse.from_json(json)
# print the JSON string representation of the object
print(GetAdditionalInputsResponse.to_json())

# convert the object into a dict
get_additional_inputs_response_dict = get_additional_inputs_response_instance.to_dict()
# create an instance of GetAdditionalInputsResponse from a dict
get_additional_inputs_response_from_dict = GetAdditionalInputsResponse.from_dict(get_additional_inputs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


