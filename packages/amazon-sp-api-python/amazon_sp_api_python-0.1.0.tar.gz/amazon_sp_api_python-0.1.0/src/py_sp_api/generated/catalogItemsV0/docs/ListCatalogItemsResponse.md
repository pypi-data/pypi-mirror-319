# ListCatalogItemsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ListMatchingItemsResponse**](ListMatchingItemsResponse.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.list_catalog_items_response import ListCatalogItemsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListCatalogItemsResponse from a JSON string
list_catalog_items_response_instance = ListCatalogItemsResponse.from_json(json)
# print the JSON string representation of the object
print(ListCatalogItemsResponse.to_json())

# convert the object into a dict
list_catalog_items_response_dict = list_catalog_items_response_instance.to_dict()
# create an instance of ListCatalogItemsResponse from a dict
list_catalog_items_response_from_dict = ListCatalogItemsResponse.from_dict(list_catalog_items_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


