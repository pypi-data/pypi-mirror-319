# GenerateTransportationOptionsResponse

The `generateTransportationOptions` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.generate_transportation_options_response import GenerateTransportationOptionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateTransportationOptionsResponse from a JSON string
generate_transportation_options_response_instance = GenerateTransportationOptionsResponse.from_json(json)
# print the JSON string representation of the object
print(GenerateTransportationOptionsResponse.to_json())

# convert the object into a dict
generate_transportation_options_response_dict = generate_transportation_options_response_instance.to_dict()
# create an instance of GenerateTransportationOptionsResponse from a dict
generate_transportation_options_response_from_dict = GenerateTransportationOptionsResponse.from_dict(generate_transportation_options_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


