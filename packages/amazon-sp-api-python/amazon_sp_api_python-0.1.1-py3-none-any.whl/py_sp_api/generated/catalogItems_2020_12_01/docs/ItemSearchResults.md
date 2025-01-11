# ItemSearchResults

Items in the Amazon catalog and search related metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number_of_results** | **int** | The estimated total number of products matched by the search query (only results up to the page count limit will be returned per request regardless of the number found).  Note: The maximum number of items (ASINs) that can be returned and paged through is 1000. | 
**pagination** | [**Pagination**](Pagination.md) |  | 
**refinements** | [**Refinements**](Refinements.md) |  | 
**items** | [**List[Item]**](Item.md) | A list of items from the Amazon catalog. | 

## Example

```python
from py_sp_api.generated.catalogItems_2020_12_01.models.item_search_results import ItemSearchResults

# TODO update the JSON string below
json = "{}"
# create an instance of ItemSearchResults from a JSON string
item_search_results_instance = ItemSearchResults.from_json(json)
# print the JSON string representation of the object
print(ItemSearchResults.to_json())

# convert the object into a dict
item_search_results_dict = item_search_results_instance.to_dict()
# create an instance of ItemSearchResults from a dict
item_search_results_from_dict = ItemSearchResults.from_dict(item_search_results_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


