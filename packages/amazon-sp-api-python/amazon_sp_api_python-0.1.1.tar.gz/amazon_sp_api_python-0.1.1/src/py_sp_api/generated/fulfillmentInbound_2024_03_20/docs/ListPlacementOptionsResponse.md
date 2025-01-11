# ListPlacementOptionsResponse

The `listPlacementOptions` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**placement_options** | [**List[PlacementOption]**](PlacementOption.md) | Placement options generated for the inbound plan. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_placement_options_response import ListPlacementOptionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListPlacementOptionsResponse from a JSON string
list_placement_options_response_instance = ListPlacementOptionsResponse.from_json(json)
# print the JSON string representation of the object
print(ListPlacementOptionsResponse.to_json())

# convert the object into a dict
list_placement_options_response_dict = list_placement_options_response_instance.to_dict()
# create an instance of ListPlacementOptionsResponse from a dict
list_placement_options_response_from_dict = ListPlacementOptionsResponse.from_dict(list_placement_options_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


