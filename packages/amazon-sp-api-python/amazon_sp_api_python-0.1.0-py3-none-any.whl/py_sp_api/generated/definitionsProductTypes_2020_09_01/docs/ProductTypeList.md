# ProductTypeList

A list of Amazon product types with definitions available.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product_types** | [**List[ProductType]**](ProductType.md) |  | 
**product_type_version** | **str** | Amazon product type version identifier. | 

## Example

```python
from py_sp_api.generated.definitionsProductTypes_2020_09_01.models.product_type_list import ProductTypeList

# TODO update the JSON string below
json = "{}"
# create an instance of ProductTypeList from a JSON string
product_type_list_instance = ProductTypeList.from_json(json)
# print the JSON string representation of the object
print(ProductTypeList.to_json())

# convert the object into a dict
product_type_list_dict = product_type_list_instance.to_dict()
# create an instance of ProductTypeList from a dict
product_type_list_from_dict = ProductTypeList.from_dict(product_type_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


