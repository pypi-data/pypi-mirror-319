# ListPackingOptionsResponse

The `listPlacementOptions` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**packing_options** | [**List[PackingOption]**](PackingOption.md) | List of packing options. | 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_packing_options_response import ListPackingOptionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListPackingOptionsResponse from a JSON string
list_packing_options_response_instance = ListPackingOptionsResponse.from_json(json)
# print the JSON string representation of the object
print(ListPackingOptionsResponse.to_json())

# convert the object into a dict
list_packing_options_response_dict = list_packing_options_response_instance.to_dict()
# create an instance of ListPackingOptionsResponse from a dict
list_packing_options_response_from_dict = ListPackingOptionsResponse.from_dict(list_packing_options_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


