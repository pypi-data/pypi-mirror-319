# ProductTypeVersion

The version details for an Amazon product type.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **str** | Version identifier. | 
**latest** | **bool** | When true, the version indicated by the version identifier is the latest available for the Amazon product type. | 
**release_candidate** | **bool** | When true, the version indicated by the version identifier is the prerelease (release candidate) for the Amazon product type. | [optional] 

## Example

```python
from py_sp_api.generated.definitionsProductTypes_2020_09_01.models.product_type_version import ProductTypeVersion

# TODO update the JSON string below
json = "{}"
# create an instance of ProductTypeVersion from a JSON string
product_type_version_instance = ProductTypeVersion.from_json(json)
# print the JSON string representation of the object
print(ProductTypeVersion.to_json())

# convert the object into a dict
product_type_version_dict = product_type_version_instance.to_dict()
# create an instance of ProductTypeVersion from a dict
product_type_version_from_dict = ProductTypeVersion.from_dict(product_type_version_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


