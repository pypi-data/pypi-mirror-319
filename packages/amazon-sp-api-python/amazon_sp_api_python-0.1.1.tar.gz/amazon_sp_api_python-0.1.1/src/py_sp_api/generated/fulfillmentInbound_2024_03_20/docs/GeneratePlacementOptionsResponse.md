# GeneratePlacementOptionsResponse

The `generatePlacementOptions` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.generate_placement_options_response import GeneratePlacementOptionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GeneratePlacementOptionsResponse from a JSON string
generate_placement_options_response_instance = GeneratePlacementOptionsResponse.from_json(json)
# print the JSON string representation of the object
print(GeneratePlacementOptionsResponse.to_json())

# convert the object into a dict
generate_placement_options_response_dict = generate_placement_options_response_instance.to_dict()
# create an instance of GeneratePlacementOptionsResponse from a dict
generate_placement_options_response_from_dict = GeneratePlacementOptionsResponse.from_dict(generate_placement_options_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


