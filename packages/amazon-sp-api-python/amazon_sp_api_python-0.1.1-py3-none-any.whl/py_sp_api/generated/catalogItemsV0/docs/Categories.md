# Categories


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product_category_id** | **str** | The identifier for the product category (or browse node). | [optional] 
**product_category_name** | **str** | The name of the product category (or browse node). | [optional] 
**parent** | **object** | The parent product category. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.categories import Categories

# TODO update the JSON string below
json = "{}"
# create an instance of Categories from a JSON string
categories_instance = Categories.from_json(json)
# print the JSON string representation of the object
print(Categories.to_json())

# convert the object into a dict
categories_dict = categories_instance.to_dict()
# create an instance of Categories from a dict
categories_from_dict = Categories.from_dict(categories_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


