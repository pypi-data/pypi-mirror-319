# GeneratePlacementOptionsRequest

The `generatePlacementOptions` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_placement** | [**List[CustomPlacementInput]**](CustomPlacementInput.md) | Custom placement options you want to add to the plan. This is only used for the India (IN - A21TJRUUN4KGV) marketplace. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.generate_placement_options_request import GeneratePlacementOptionsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GeneratePlacementOptionsRequest from a JSON string
generate_placement_options_request_instance = GeneratePlacementOptionsRequest.from_json(json)
# print the JSON string representation of the object
print(GeneratePlacementOptionsRequest.to_json())

# convert the object into a dict
generate_placement_options_request_dict = generate_placement_options_request_instance.to_dict()
# create an instance of GeneratePlacementOptionsRequest from a dict
generate_placement_options_request_from_dict = GeneratePlacementOptionsRequest.from_dict(generate_placement_options_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


