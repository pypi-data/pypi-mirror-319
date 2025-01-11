# GetCatalogItemResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**Item**](Item.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.get_catalog_item_response import GetCatalogItemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetCatalogItemResponse from a JSON string
get_catalog_item_response_instance = GetCatalogItemResponse.from_json(json)
# print the JSON string representation of the object
print(GetCatalogItemResponse.to_json())

# convert the object into a dict
get_catalog_item_response_dict = get_catalog_item_response_instance.to_dict()
# create an instance of GetCatalogItemResponse from a dict
get_catalog_item_response_from_dict = GetCatalogItemResponse.from_dict(get_catalog_item_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


