# ListMatchingItemsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[Item]**](Item.md) | A list of items. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.list_matching_items_response import ListMatchingItemsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListMatchingItemsResponse from a JSON string
list_matching_items_response_instance = ListMatchingItemsResponse.from_json(json)
# print the JSON string representation of the object
print(ListMatchingItemsResponse.to_json())

# convert the object into a dict
list_matching_items_response_dict = list_matching_items_response_instance.to_dict()
# create an instance of ListMatchingItemsResponse from a dict
list_matching_items_response_from_dict = ListMatchingItemsResponse.from_dict(list_matching_items_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


