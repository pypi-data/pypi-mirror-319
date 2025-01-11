# ListCatalogCategoriesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**List[Categories]**](Categories.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.list_catalog_categories_response import ListCatalogCategoriesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListCatalogCategoriesResponse from a JSON string
list_catalog_categories_response_instance = ListCatalogCategoriesResponse.from_json(json)
# print the JSON string representation of the object
print(ListCatalogCategoriesResponse.to_json())

# convert the object into a dict
list_catalog_categories_response_dict = list_catalog_categories_response_instance.to_dict()
# create an instance of ListCatalogCategoriesResponse from a dict
list_catalog_categories_response_from_dict = ListCatalogCategoriesResponse.from_dict(list_catalog_categories_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


